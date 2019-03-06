import React from 'react';
import {
    Activity,
    CommentField, CommentList,
    FlatFeed,
    LikeButton,
    StatusUpdateForm,
} from "react-activity-feed";
class UnApprovedGroup extends React.Component {
    constructor(props) {
        super(props);
        console.log("inside unapproved", this.props)


    }
    getCookie(name) {
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
    feedrequest(client, feedGroup, userId, options) {
        var url = new URL(window.location.origin+'/getfeed/'+feedGroup+'/'+userId);
        delete options['reactions'];
        url.search = new URLSearchParams(options)
        console.log(url)
        return fetch(url).then(result =>{
            console.log(result)
            return result.json()
        })
    }
    render () {
        console.log("came into feed");
    return (
        <React.Fragment>
         <FlatFeed
          feedGroup = "globalgroup"
          userId = { this.props.match.params.groupid }
          doFeedRequest = {this.feedrequest}
          Activity={(props) =>
              <Activity {...props}
                Footer={() => (
                  <div style={ {padding: '8px 16px'} }>
                  </div>
                )}
              />
            }
          />

            </React.Fragment>

    )
  }
}
export default UnApprovedGroup
