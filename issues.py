import os
import requests
from datetime import datetime

# Account 1 credentials
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_OWNER = "sydneylin12"
REPO_NAME = "pull-shark"

# Account 2 credentials
SECOND_GITHUB_TOKEN = os.getenv('SECOND_GITHUB_TOKEN')
SECOND_REPO_OWNER = "sydneylin3"
SECOND_REPO_NAME = "sydneylin3"

# Github GraphQL API endpoint
url = "https://api.github.com/graphql"

# Define headers for the GitHub API request
baseHeaders = {
    "Content-Type": "application/json"
}
firstAccountHeaders = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    **baseHeaders
}
secondAccountHeaders = {
    "Authorization": f"Bearer {SECOND_GITHUB_TOKEN}",
    **baseHeaders
}

# Creates a github discussion in account 2 and returns the discussion ID
def createDiscussion():
    get_repo_and_categories_query = """
        query {
            repository(owner: "%s", name: "%s") {
                id
                discussionCategories(first: 10) {
                    nodes {
                        id
                        name
                    }
                }
            }
        }
    """ % (SECOND_REPO_OWNER, SECOND_REPO_NAME)

    # Fetch repository and discussion categories
    response = requests.post(url, headers=secondAccountHeaders, json={"query": get_repo_and_categories_query})
    repo_data = response.json()

    if 'errors' in repo_data:
        print(f"Error: {repo_data['errors']}")
    else:
        repo_id = repo_data['data']['repository']['id']
        print(f"Repository ID: {repo_id}")
        
        # Find the categoryId for the Q&A category
        categories = repo_data['data']['repository']['discussionCategories']['nodes']
        qna_category_id = None
        for category in categories:
            if category['name'].lower() == 'q&a':
                qna_category_id = category['id']
                break

        if not qna_category_id:
            print("Error: Q&A category not found.")
            return
        
        print(f"Q&A Category ID: {qna_category_id}")    
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        title = f"Test discussion: {time}"
        body = f"Test question: {time}"

        create_discussion_mutation = """
            mutation {
                createDiscussion(input: {
                    repositoryId: "%s",
                    title: "%s",
                    body: "%s",
                    categoryId: "%s"
                }) {
                    discussion {
                        id
                    }
                }
            }
        """ % (repo_id, title, body, qna_category_id)

        create_discussion_response = requests.post(url, headers=secondAccountHeaders, json={"query": create_discussion_mutation})
        discussion_data = create_discussion_response.json()
        
        if 'errors' in discussion_data:
            print(f"Error: {discussion_data['errors']}")
        else:
            discussion_id = discussion_data['data']['createDiscussion']['discussion']['id']
            print(f"Q&A Discussion created with ID: {discussion_id}")
            return discussion_id
            
def commentOnDiscussion(discussion_id):
    solution = "Here is a solution!"
    post_comment_mutation = """
        mutation {
            addDiscussionComment(input: {
                discussionId: "%s",
                body: "%s"
            }) {
                comment {
                    id
                }
            }
        }
    """ % (discussion_id, solution)

    # Post the comment on the discussion
    response = requests.post(url, headers=firstAccountHeaders, json={"query": post_comment_mutation})
    comment_data = response.json()

    if 'errors' in comment_data:
        print(f"Error: {comment_data['errors']}")
    else:
        comment_id = comment_data['data']['addDiscussionComment']['comment']['id']
        print(f"Comment posted with ID: {comment_id}")
        return comment_id

def markAnswered(commentId):
    mark_answer_mutation = """
        mutation {
            markDiscussionCommentAsAnswer(input: {
                id: "%s"
            }) {
                discussion {
                    url
                }
            }
        }
    """ % commentId
     
    response = requests.post(url, headers=secondAccountHeaders, json={"query": mark_answer_mutation})
    data = response.json()

    if 'errors' in data:
       print(f"Error: {data['errors']}")
    else:
        discussion_url = data['data']['markDiscussionCommentAsAnswer']['discussion']['url']
        print(f"Comment marked as the accepted answer for discussion '{discussion_url}'")
 
def main():
    id = createDiscussion()
    commentId = commentOnDiscussion(id)
    markAnswered(commentId)

if __name__ == "__main__":
    for i in range (48):
        main()
