import UnApprovedGroup from "./components/Group";
import React from "react";
import {Activity, CommentField, CommentList, FlatFeed, LikeButton, StatusUpdateForm} from "react-activity-feed";
import * as moment from "moment";

export function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
export function feedrequest(client, feedGroup, userId, options) {
    var url = new URL(window.location.origin+'/youngwall/getfeed/'+feedGroup+'/'+userId);
    delete options['reactions'];
    url.search = new URLSearchParams(options)
    return fetch(url).then(result =>{
        return result.json()
    })
}
export function doupdaterequest(params, feedgroup, feedid) {
    console.log(params.actor)
    params.actor = 'SU:'+params.actor.id
    console.log(params)
    var url = new URL(window.location.origin+'/youngwall/getfeed/'+ feedgroup +'/'+ feedid);
    var csrftoken = getCookie('csrftoken');

    return fetch(url, {
        credentials: 'include',
        headers: {
            contentType: 'application/json; charset=utf-8',
            'X-CSRFToken': csrftoken
        },
        method:"post",
        body: JSON.stringify(params),

    }).then(result =>{
        console.log(result)
        return result.json()
    })
}
export function handlefollow(from_page, to_page, type_of_page) {
    var csrftoken = getCookie('csrftoken');
    var params =  {
        from_page: from_page,
        to_page: to_page,
        type_of_page: type_of_page
    };
    fetch("/youngwall/follow/",{
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json; charset=utf-8',
            'X-CSRFToken': csrftoken
        },
        method:"post",
        body: JSON.stringify(params),

    })
        .then(res => res.json())
        .then((result) => {
                console.log(result)
            },
            (error) => {
                console.log(error)
            })
}

export function removeComment(id) {
    fetch("/youngwall/delete_reaction?id=" + id).then((res) => res);
}

export function humanizeTimestamp(timestamp) {
  const time = moment.utc(timestamp); // parse time as UTC
  const now = moment();
  // Not in future humanized time
  return moment.min(time, now).from(now);
}
