/**
 * function to get the csrf token
 * @param name
 * @returns {null}
 */
const getCookie = (name) => {
  let cookieValue = null
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}

/**
 * Calling the api for sending a friend request to the user.
 * @param username
 */
const sendFriendRequest = (username) => {
  $.ajax({
    type: 'POST',
    dataType: 'json',
    url: '/friend/send_friend_request/',
    timeout: 3000,
    data: {
      csrfmiddlewaretoken: getCookie('csrftoken'),
      receiver: username
    },
    success: function (data) {
      console.log('success: ' + data.response)
    },
    error: function (data) {
      console.log('error: ' + data.response)
    },
    complete: function (data) {
      console.log('complete: ' + data.response)
      reloadPage()
    }
  })
}

/**
 * Calling the api for accepting the friend request sent by the user
 * @param request_id
 */

const acceptFriendRequest = (request_id) => {
  $.ajax({
    type: 'POST',
    dataType: 'json',
    url: '/friend/accept_friend_request/',
    timeout: 3000,
    data: {
      csrfmiddlewaretoken: getCookie('csrftoken'),
      request_id: request_id
    },
    success: function (data) {
      console.log('success: ' + data.response)
    },
    error: function (data) {
      console.log('error: ' + data.response)
    },
    complete: function (data) {
      console.log('complete: ' + data.response)
      reloadPage()
    }
  })
}

/**
 * Calling the api for declining the friend request sent by the user
 * @param request_id
 */
const declineFriendRequest = (request_id) => {
  $.ajax({
    type: 'POST',
    dataType: 'json',
    url: '/friend/decline_friend_request/',
    timeout: 3000,
    data: {
      csrfmiddlewaretoken: getCookie('csrftoken'),
      request_id: request_id
    },
    success: function (data) {
      console.log('success: ' + data.response)
    },
    error: function (data) {
      console.log('error: ' + data.response)
    },
    complete: function (data) {
      console.log('complete: ' + data.response)
      reloadPage()
    }
  })
}

/**
 * Calling the api for canceling the friend request sent by the user
 * @param request_id
 */
const cancelFriendRequest = (request_id) => {
  $.ajax({
    type: 'POST',
    dataType: 'json',
    url: '/friend/cancel_friend_request/',
    timeout: 3000,
    data: {
      request_id: request_id,
      csrfmiddlewaretoken: getCookie('csrftoken')
    },
    success: function (data) {
      console.log('success: ' + data.response)
    },
    error: function (data) {
      console.log('error: ' + data.response)
    },
    complete: function (data) {
      console.log('complete: ' + data.response)
      reloadPage()
    }
  })
}

/**
 * Calling an api for upvoting / liking the post shared by the users
 * @param post_id
 */
const upvoteUserPost = (post_id) => {
  $.ajax({
    type: 'POST',
    dataType: 'json',
    url: '/upvote_post/',
    timeout: 3000,
    data: {
      post_id: post_id,
      csrfmiddlewaretoken: getCookie('csrftoken')
    },
    success: function (data) {
      console.log('success: ' + data.response)
    },
    error: function (data) {
      console.log('error: ' + data.response)
    },
    complete: function (data) {
      console.log('complete: ' + data.response)
      window.location = "/"
    }
  })
}

/**
 * reloading the page after a successful request to update the page
 */
function reloadPage() {
  location.reload()
}
