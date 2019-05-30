import React from 'react';
import {
    Activity,
    CommentField, CommentList,
    FlatFeed,
    LikeButton,
    StatusUpdateForm, StreamApp,
} from "react-activity-feed";
import {doupdaterequest, feedrequest, getCookie, handlefollow} from "../../utils";
import UserBar from "../YSUserBar";
import RedirectTimeline from "../RedirectTimeline";
class SchoolFeed extends React.Component {
    constructor(props) {
        super(props);

    }
    render () {
        console.log("came into school");
        console.log(this.props)
        return (
            <React.Fragment>
                <div className="section__dash"></div>
                <h1 className="section__title" style={{fontSize: '1.25rem'}}>{this.props.section_title} </h1>
                <StreamApp
                    apiKey= {this.props.apiKey}
                    appId= {this.props.appId}
                    token= {this.props.social_token}
                >
                    <div id="react-feed">
                        <FlatFeed
                            options={{reactions: { recent: true } }}
                            feedGroup = {this.props.feedgroup}
                            userId = { this.props.feedid }
                            doFeedRequest = {feedrequest}
                            Activity={(props) =>
                                <Activity {...props}
                                          Header={() => (
                                              <UserBar {...props} parent={"schooldash"} />
                                          )}

                                />
                            }
                            Paginator={(props) =>
                                <RedirectTimeline {...props} schoolpage={true}/>}

                        />
                    </div>
                </StreamApp>
            </React.Fragment>

        )
    }
}
export default SchoolFeed
