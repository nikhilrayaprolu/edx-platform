import React from 'react';
import {
    Activity,
    CommentField, CommentList,
    FlatFeed,
    LikeButton,
    StatusUpdateForm,
} from "react-activity-feed";
import {browserHistory} from 'react-router';
import {withRouter} from "react-router-dom";
import UserBar from "../YSUserBar";
class Home extends React.Component {

    render () {
        console.log("came into home")
    return (
        <React.Fragment>
        <StatusUpdateForm
          feedGroup="user"
        />
         <FlatFeed
          options={{reactions: { recent: true } }}
          notify
          Activity={(props) =>
              <Activity {...props}
                  onClickUser = {(user) => {console.log(user);this.props.history.push(user.id)}}
                        Header={() => (
                                          <UserBar {...props} />
                                      )}
                Footer={() => (
                  <div style={ {padding: '8px 16px'} }>
                    <LikeButton {...props} />
                    <CommentField
                      activity={props.activity}
                      onAddReaction={props.onAddReaction} />
                    <CommentList activityId={props.activity.id} />
                  </div>
                )}
              />
            }
          />

            </React.Fragment>

    )
  }
}
export default withRouter(Home)
