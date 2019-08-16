import React from 'react';
import {
    Activity,
    CommentField, CommentList,
    FlatFeed,
    LikeButton,
    StatusUpdateForm, StreamApp,
} from "react-activity-feed";
import UserBar from "../YSUserBar";
import RedirectTimeline from "../RedirectTimeline";
class Feed extends React.Component {
    render () {
        console.log("came into feed", this.props);
        return (
            <React.Fragment>
                <div className="section__dash"></div>
                <h1 className="section__title">{this.props.section_title} </h1>
                <StreamApp
        apiKey= {this.props.apiKey}
        appId= {this.props.appId}
        token= {this.props.social_token}
      >
                <FlatFeed
                    options={{reactions: { recent: true } }}
                    feedGroup = "timeline"
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
                    Paginator={(props) =>
                        <RedirectTimeline {...props} />}

                />
                </StreamApp>

            </React.Fragment>

        )
    }
}
export default Feed
