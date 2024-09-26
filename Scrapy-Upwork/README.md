Simple Upwork vacancies parser that grabs the content from https://www.upwork.com/freelance-jobs/.

The spider goes all over the categories and scraps vacancies from each of them.

For presentation purposes I limited the number of categories to only one, so the process doesn't take a while.

You may check out the output of the program in the <code>upwork.json</code> file or generate a fresh one executing <br/>
<code>scrapy crawl upwork_spider -o <your_file_name>.json</code>
