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

export let context = {
    "user_position": {
        "position": 1,
        "score": 10
    },
    "school": "testschool2",
    "apiKey": "ed97ces2ru44",
    "class_average_score": 0,
    "schoolpage": "testschool2",
    "young_skills": [
        {
            "created": "2019-05-28T10:44:22.077644Z",
            "mode": "audit",
            "is_active": true,
            "course_details": {
                "course_id": "course-v1:edX+DemoX+Demo_Course",
                "course_name": "edX Demonstration Course",
                "enrollment_start": null,
                "enrollment_end": null,
                "course_start": "2013-02-05T05:00:00Z",
                "course_end": null,
                "invite_only": false,
                "course_modes": [
                    {
                        "slug": "audit",
                        "name": "Audit",
                        "min_price": 0,
                        "suggested_prices": "",
                        "currency": "usd",
                        "expiration_datetime": null,
                        "description": null,
                        "sku": null,
                        "bulk_sku": null
                    }
                ],
                "course_image_url": "/asset-v1:edX+DemoX+Demo_Course+type@asset+block@images_course_image.jpg"
            },
            "user": "9959485499"
        },
        {
            "created": "2019-05-28T10:43:25.335319Z",
            "mode": "audit",
            "is_active": true,
            "course_details": {
                "course_id": "course-v1:iiit+iiit+iiit",
                "course_name": "Library_class_10_math",
                "enrollment_start": null,
                "enrollment_end": null,
                "course_start": "2019-01-01T00:00:00Z",
                "course_end": null,
                "invite_only": false,
                "course_modes": [
                    {
                        "slug": "audit",
                        "name": "Audit",
                        "min_price": 0,
                        "suggested_prices": "",
                        "currency": "usd",
                        "expiration_datetime": null,
                        "description": null,
                        "sku": null,
                        "bulk_sku": null
                    }
                ],
                "course_image_url": "/asset-v1:iiit+iiit+iiit+type@asset+block@images_course_image.jpg"
            },
            "user": "9959485499"
        }
    ],
    "social_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiOTk1OTQ4NTQ5OSJ9.gL_VGJ2cPpUaSn1WScrD12gODpLHS0jarlvMWw8b3vA",
    "userid": "9959485499",
    "user_engagement_score": 10,
    "resume_button_urls": [
        "",
        ""
    ],
    "appId": "48327",
    "course_enrollments": [
        {
            "created": "2019-05-18T13:12:27.455377Z",
            "mode": "audit",
            "is_active": true,
            "course_details": {
                "course_id": "course-v1:testschool2+maths6+3",
                "course_name": "maths6",
                "enrollment_start": null,
                "enrollment_end": null,
                "course_start": "2019-01-01T00:00:00Z",
                "course_end": null,
                "invite_only": false,
                "course_modes": [
                    {
                        "slug": "audit",
                        "name": "Audit",
                        "min_price": 0,
                        "suggested_prices": "",
                        "currency": "usd",
                        "expiration_datetime": null,
                        "description": null,
                        "sku": null,
                        "bulk_sku": null
                    }
                ],
                "course_image_url": "/asset-v1:testschool2+maths6+3+type@asset+block@images_course_image.jpg"
            },
            "user": "9959485499"
        },
        {
            "created": "2019-05-17T01:49:42.446926Z",
            "mode": "audit",
            "is_active": true,
            "course_details": {
                "course_id": "course-v1:testschool2+Maths+2",
                "course_name": "Maths",
                "enrollment_start": null,
                "enrollment_end": null,
                "course_start": "2019-01-01T00:00:00Z",
                "course_end": null,
                "invite_only": false,
                "course_modes": [
                    {
                        "slug": "audit",
                        "name": "Audit",
                        "min_price": 0,
                        "suggested_prices": "",
                        "currency": "usd",
                        "expiration_datetime": null,
                        "description": null,
                        "sku": null,
                        "bulk_sku": null
                    }
                ],
                "course_image_url": "/asset-v1:testschool2+Maths+2+type@asset+block@images_course_image.jpg"
            },
            "user": "9959485499"
        }
    ],
    "leaderboard": {
        "total_user_count": 37,
        "queryset": [
            {
                "user__username": "9959485499",
                "score": 10,
                "user__id": 687,
                "modified": "2019-05-27T07:16:32.132021Z",
                "user__mini_user_profile__first_name": "B. AKSHAYA"
            }
        ],
        "course_avg": 0
    }
}
