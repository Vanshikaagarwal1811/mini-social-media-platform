console.log("SCRIPT LOADED")

showLoggedInUser()

// LOAD POSTS

fetch('http://127.0.0.1:8000/posts/')
.then(response => response.json())
.then(data => {

    let postsDiv = document.getElementById('posts')

    postsDiv.innerHTML = ''

    data.forEach(post => {

        let commentsHTML = ''

        post.comments.forEach(comment => {

            commentsHTML += `
                <p>💬 ${comment.text}</p>
            `
        })

        postsDiv.innerHTML += `

            <div class="post">

                <h4>👤 ${post.username}</h4>

                <h3>${post.caption}</h3>

                ${post.image ? `
                <img
                    src="http://127.0.0.1:8000${post.image}"
                    width="300"
                >
                ` : ''}

                <br><br>

                <button onclick="likePost(${post.id})">
                    ❤️ ${post.likes.length}
                </button>

                <button onclick="deletePost(${post.id})">
                    🗑️ Delete
                </button>

                <br><br>

                <input
                    type="text"
                    id="comment-${post.id}"
                    placeholder="Add comment"
                >

                <button onclick="addComment(${post.id})">
                    💬 Comment
                </button>

                <h4>Comments:</h4>

                <div class="comments">
                    ${commentsHTML}
                </div>

            </div>

            <hr>

        `
    })

})

// LOGIN

function login(){

    let username =
    document.getElementById('username').value

    let password =
    document.getElementById('password').value

    fetch('http://127.0.0.1:8000/login/', {

        method: 'POST',

        headers: {
            'Content-Type': 'application/json'
        },

        body: JSON.stringify({
            username: username,
            password: password
        })

    })

    .then(response => response.json())

    .then(data => {

        localStorage.setItem(
            'token',
            data.access
        )

        alert('Login Successful')

        location.reload()

    })

}

// CREATE POST

function createPost() {

    let caption =
    document.getElementById('caption').value

    let image =
    document.getElementById('image').files[0]

    let formData = new FormData()

    formData.append('caption', caption)

    if(image){
        formData.append('image', image)
    }

    fetch('http://127.0.0.1:8000/create-post/', {

        method: 'POST',

        headers: {

            'Authorization':
            `Bearer ${localStorage.getItem('token')}`
        },

        body: formData

    })

    .then(response => response.json())

    .then(data => {

        location.reload()

    })

}

// LIKE POST

function likePost(postId){

    fetch(`http://127.0.0.1:8000/like-post/${postId}/`, {

        method: 'POST',

        headers: {

            'Authorization':
            `Bearer ${localStorage.getItem('token')}`
        }

    })

    .then(response => response.json())

    .then(data => {

        location.reload()

    })

}

// DELETE POST

function deletePost(postId){

    fetch(
        `http://127.0.0.1:8000/delete-post/${postId}/`,
        {

            method: 'DELETE',

            headers: {

                'Authorization':
                `Bearer ${localStorage.getItem('token')}`
            }
        }
    )

    .then(response => response.json())

    .then(data => {

        location.reload()

    })

}

// ADD COMMENT

function addComment(postId){

    let text = document.getElementById(`comment-${postId}`).value

    fetch(`http://127.0.0.1:8000/comment/${postId}/`, {

        method: 'POST',

        headers: {

            'Content-Type': 'application/json',

            'Authorization':
            `Bearer ${localStorage.getItem('token')}`
        },

        body: JSON.stringify({
            text: text
        })

    })

    .then(response => response.json())

    .then(data => {

        location.reload()

    })

}

// GET PROFILE

function getProfile(){

    let username =
    document.getElementById('profileUsername').value

    fetch(
        `http://127.0.0.1:8000/profile/${username}/`
    )

    .then(response => response.json())

    .then(data => {

        let profileDiv =
        document.getElementById('profile')

        profileDiv.innerHTML = `

            <h2>
                ${data.user.username}
            </h2>

            <p>
                ${data.user.email}
            </p>

            <p>
                Followers:
                ${data.user.followers_count}
            </p>

            <p>
                Following:
                ${data.user.following_count}
            </p>

            <button onclick="followUser(${data.user.id})">
                Follow / Unfollow
            </button>

            <br><br>

        `

        data.posts.forEach(post => {

            profileDiv.innerHTML += `

                <div class="post">

                    <h4>
                        👤 ${post.username}
                    </h4>

                    <h3>
                        ${post.caption}
                    </h3>

                    ${post.image ? `
                    <img
                        src="http://127.0.0.1:8000${post.image}"
                        width="300"
                    >
                    ` : ''}

                    <p>
                        ❤️ ${post.likes.length}
                    </p>

                </div>

                <hr>

            `
        })

    })

}

// FOLLOW USER

function followUser(userId){

    fetch(
        `http://127.0.0.1:8000/follow/${userId}/`,
        {

            method: 'POST',

            headers: {

                'Authorization':
                `Bearer ${localStorage.getItem('token')}`
            }
        }

    )

    .then(response => response.json())

    .then(data => {

        alert(data.message)

        getProfile()

    })

}

// LOGOUT

function logout(){

    localStorage.removeItem('token')

    alert('Logged out successfully')

    location.reload()

}

// LOGIN STATUS

function showLoggedInUser(){

    let token = localStorage.getItem('token')

    if(token){

        document.getElementById(
            'welcomeUser'
        ).innerHTML =

        "🟢 Logged In"

    }

    else{

        document.getElementById(
            'welcomeUser'
        ).innerHTML =

        "🔴 Not Logged In"

    }

}