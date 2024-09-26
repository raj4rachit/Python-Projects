import React from 'react';
import axios from 'axios';
import * as projects from '../../../services/projectsService';
import AddMembersForm from './AddMembersForm';
import DeleteProjectButton from './DeleteProjectButton';
import { Link } from 'react-router-dom';
import {
    Spinner,
    Card,
    Table,
    CardHeader,
    CardFooter,
    CardBody,
    CardTitle,
    CardText
} from 'reactstrap';
import { NotFound } from '../../Pages';


export default class ProjectDetail extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            user: props.user,
            name: undefined,
            description: undefined,
            members: [],
            employeeStatuses: {},
            socket: undefined,
        };
        this.reqSource = undefined;
        this._isMounted = false;
    }

    setState = (...args) => {
        if (this._isMounted) {
            super.setState(...args);
        }
    };

    initWebsocket() {
        const { host, protocol } = location;
        const url = `${protocol === "http:" ? "ws" : "wss"}://${host}/master/`;
        console.log("Connecting to ", url);

        const socket = new WebSocket(url);

        socket.onopen = event => {
            for (let id in this.state.employeeStatuses) {
                socket.send(JSON.stringify({
                    type: "employee.ping",
                    user_id: id
                }));
            }
        };

        socket.onmessage = event => {
            const data = JSON.parse(event.data);
            switch(data.type) {
                case "websocket.accept": {
                    console.log("Websocket connection established. ");
                    break;
                }
                case "employee.status": {
                    const prevStatuses = this.state.employeeStatuses;
                    this.setState({employeeStatuses: {...prevStatuses, [data.user_id]: data.status}});
                    break;
                }
                default: {
                    console.log("Unknown message of type: ", data.type);
                }
            }
        };
        socket.onclose = event => {
            console.warn("Websocket connection closed. ", event.reason);
        };

        socket.onerror = event => {
            console.error("Websocket error. ", event.reason);
        };

        this.setState({socket});
    }

    loadProjectInfo = async id => {
        await this.cancelPreviousRequests();
        try {
            const response = await projects.getProject(id, this.reqSource.token);
            const data = JSON.parse(response.data);

            const employeeStatuses = {};
            data.members.forEach(m => {
                employeeStatuses[m.id] = "offline";
            });
            this.setState({
                ...data,
                employeeStatuses
            });
        } catch (error) {
            console.error(error.message);
            if (error.response.status === 400) {
                const fieldErrors = error.response.data;
                Object.keys(fieldErrors).map((fieldName) => {
                    fieldErrors[fieldName] = fieldErrors[fieldName].join(" ");
                    // console.log(fieldErrors[fieldName]);
                });

                this.setState({
                    errors: fieldErrors
                });
            }
        }
    };

    handleProjectDeleted = async () => {
        await this.cancelPreviousRequests();
        history.back();
    };

    cancelPreviousRequests = async () => {
        if (this.reqSource) {
            this.reqSource.cancel();
        }
        this.reqSource = axios.CancelToken.source();
    };

    async componentDidMount() {
        this._isMounted = true;
        const { match: { params } } = this.props;
        await this.loadProjectInfo(params.id);
        this.initWebsocket();
    }

    async componentWillUnmount() {
        this._isMounted = false;
        await this.cancelPreviousRequests();
        if (this.state.socket !== undefined) {
            this.state.socket.close();
        }
    }

    renderMembersTable() {
        const { user, members, employeeStatuses } = this.state;
        if (members === undefined) {
            console.error("renderMembersTable() called when information about the project was not loaded");
            return;
        }

        return (
            <div>
                <Table>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Username</th>
                            <th>Status</th>
                            <th>Email</th>
                            <th>Account Registration Date</th>
                        </tr>
                    </thead>
                    <tbody>
                        {members.map((m, idx) => (
                            <tr className={m.is_staff ? "staff-user" : ""} key={`${m.id}`}>
                                <th scope="row">{idx + 1}</th>
                                <td>
                                    <Link
                                        to={m.id === user.id ? "/dashboard/profile" : `/dashboard/activity-logs/user/${m.id}`}
                                        className="username-link"
                                    >
                                        {m.id === user.id ? (
                                            <React.Fragment>
                                                @{m.username}
                                                <span className="font-weight-bolder" style={{fontSize: "0.9rem"}}> (You)</span>
                                            </React.Fragment>
                                        ) : (
                                                <React.Fragment>@{m.username}</React.Fragment>
                                            )}

                                    </Link>
                                </td>
                                <td className={`text-center ${employeeStatuses[m.id]}`}>{employeeStatuses[m.id]}</td>
                                <td>{m.email || <span className="text-secondary">No email provided.</span>}</td>
                                <td>{new Date(Date.parse(m.date_joined)).toLocaleString()}</td>
                            </tr>
                        ))}
                    </tbody>
                </Table>
                <div className="color-explained d-flex">
                    <span className="staff-user disabled d-inline-block" style={{width: "20px", height: "20px"}}/>
                    <span className="d-inline-block small ml-sm-1">- staff users</span>
                </div>
            </div>
        );
    }

    render() {
        const { id, name, description } = this.state;

        if (id === undefined) {
            return <Spinner/>
        }
        if (id === null) {
            return <NotFound/>
        }

        return (
            <Card>
                <CardHeader className="d-flex justify-content-between">
                    <h3>{name}</h3>
                    <DeleteProjectButton projectId={id} onProjectDeleted={this.handleProjectDeleted}/>
                </CardHeader>
                <CardBody>
                    <CardTitle className="font-italic">Description:</CardTitle>
                    <CardText>{description}</CardText>

                    <CardTitle className="font-italic d-flex justify-content-between align-items-end">
                        Members:
                        <AddMembersForm
                            projectId={id}
                            onMembersAdded={updatedProjectData => {this.setState({...updatedProjectData});}}
                        />
                    </CardTitle>
                    {this.renderMembersTable()}
                </CardBody>
                <CardFooter>
                    <span style={{visibility: "hidden"}}>
                        Owners:
                    </span>
                </CardFooter>
            </Card>
        );
    }
};

