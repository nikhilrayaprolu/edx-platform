import React from 'react';
import {
    Activity,
    CommentField, CommentList,
    FlatFeed,
    LikeButton,
    StatusUpdateForm,
} from "react-activity-feed";
import {doupdaterequest, feedrequest} from "../../utils";
import UserBar from "../YSUserBar";
class CourseGroup extends React.Component {
    constructor(props) {
        super(props);
        this.doupdaterequest = this.doupdaterequest.bind(this)
        this.feedid = this.props.match.params.courseid.replace(/\+/g,'-').replace(':', '-');
        this.feedgroup = 'course'
    }
    doupdaterequest(params) {
        doupdaterequest(params, this.feedgroup, this.feedid)
    }
    render () {
        return (
            <React.Fragment>
                <div id="react-feed">
                    <StatusUpdateForm
                        feedGroup={ this.feedgroup }
                        userId = { this.feedid }
                        doRequest = { this.doupdaterequest}
                    />
                    <FlatFeed
                        options={{reactions: { recent: true } }}
                        feedGroup = { this.feedgroup }
                        userId = { this.feedid }
                        doFeedRequest = {feedrequest}
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
                </div>

            </React.Fragment>

        )
    }
}
export default CourseGroup
