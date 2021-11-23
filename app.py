from flask import Flask, request, render_template
import requests
app = Flask(__name__)


def run_query(input_login):
    headers = {"Authorization": "token token from GitHub"}
    query = """
    {
      repositoryOwner(login: "%s") {
        ... on User {
        name
          repositories(first: 100) {
            edges {
              node {
                name
              }
            }
          }
        }
      }
    }
    """ % input_login
    request_to_github = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    print(request_to_github)
    if request_to_github.status_code == 200:
        return request_to_github.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request_to_github.status_code, query))


@app.route('/', methods=['POST', 'GET'])
def get_phone():
    name = ''
    repos = []
    if request.method == 'POST':
        try:
            github_login = request.form.get('GitHub_login')
            print(github_login)
            data_from_github = run_query(github_login)
            print(data_from_github)
            name = data_from_github['data']['repositoryOwner']['name']
            repos = data_from_github['data']['repositoryOwner']['repositories']['edges']
        except:
            name = 'No such account exists'
    return render_template('index.html', name=name, repos=repos)


if __name__ == '__main__':
    app.run(debug=True)
