import React from 'react';
import {
    Activity,
    CommentField, CommentList,
    FlatFeed,
    LikeButton,
    StatusUpdateForm,
} from "react-activity-feed";
import UserBar from "../YSUserBar";
class Feed extends React.Component {
    render () {
        console.log("came into feed");
        return (
            <React.Fragment>
                <FlatFeed
                    options={{reactions: { recent: true } }}
                    feedGroup = "user"
                    userId = {this.props.match.params.userid}
                    notify
                    Activity={(props) =>
                        <Activity {...props}
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
export default Feed
