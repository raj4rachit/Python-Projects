import React, { Component } from 'react';
import BaseRouter from '../routes';
import Layout from '../containers/Layout'
import { getUserAccount, logoutUser } from "../services/authService";
import 'bootstrap/dist/css/bootstrap.css';
import '../App.css';


class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            loadingUser: true,
            user: undefined
        };
    }

    tryRestoreSession = async () => {
        try {
            const response = await getUserAccount();
            const user = JSON.parse(response.data);
            this.setState({
                user: user
            });
        } catch (error) {
            if (error.response.status === 401 || error.response.status === 403) {
                console.error("Couldn't restore session.", error.response.statusText);
            } else {
                console.error("Unexpected server response when retrieving user account.");
            }
        }

        this.setState({loadingUser: false});
    };

    async componentDidMount() {
        await this.tryRestoreSession();
    }

    handleLogin = (user) => {
        this.setState({
            user: user
        });
    };

    handleLogout = async () => {
        await logoutUser();
        this.setState({
            user: {
                token: null
            }
        });
    };

    render() {
        if (this.state.loadingUser) {
            return <div>Loading...</div>
        }
        const { user } = this.state;
        // console.log(user, 'User (App component)');
        return (
            <React.Fragment>
                <Layout user={user}>
                    <BaseRouter
                        user={user}
                        onLogin={this.handleLogin}
                        onLogout={this.handleLogout}
                    />
                </Layout>
            </React.Fragment>
        );
    }
}

export default App;