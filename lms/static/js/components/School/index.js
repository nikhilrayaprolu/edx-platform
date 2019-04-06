import React from 'react';
import {
    Activity,
    CommentField, CommentList,
    FlatFeed,
    LikeButton,
    StatusUpdateForm,
} from "react-activity-feed";
import {doupdaterequest, feedrequest, getCookie, handlefollow} from "../../utils";
import UserBar from "../YSUserBar";
class SchoolFeed extends React.Component {
    constructor(props) {
        super(props);
        this.doupdaterequest = this.doupdaterequest.bind(this);
        this.state = {
            error: null,
            isLoaded: false,
            ismoderator: false,
            user_profile: null,
            group_details: null,
            following: false,
        };
        this.feedid = this.props.match.params.schoolid || window.schoolpage;
        this.feedgroup = "school"
        this.handlefollow = this.handlefollow.bind(this);
    }
    componentDidMount() {
        var csrftoken = getCookie('csrftoken');
        fetch("/youngwall/moderator/"+this.feedid)
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({
                        isLoaded: true,
                        ismoderator: result.ismoderator,
                        user_profile: result.user_profile,
                        group_details: result.group_details,
                        following: result.following,
                    });
                },
                (error) => {
                    this.setState({
                        isLoaded: true,
                        error
                    })
                }
            )
    }
    doupdaterequest(params) {
            doupdaterequest(params, this.feedgroup, this.feedid)
    }
    handlefollow(id) {
        handlefollow(this.state.user_profile.page_id, this.feedid, 'school');
        this.setState(prevstate => ({ ...prevstate, following: !prevstate.following }))

    }
    schoolcard() {
        return (
            <React.Fragment>
                { this.state.group_details ? (
                    <div className="card ys-card">
                        <img className="card-img-top ys-group-card-img-top" src="http://www.gstatic.com/tv/thumb/persons/1083/1083_v9_ba.jpg" alt="Card image cap" />
                        <div className="card-body">
                            <h5 className="card-title">{this.state.group_details.schoolname}</h5>
                            <p className="card-text">{this.state.group_details.description}</p>
                            <button className="btn btn-success" onClick={() => {this.handlefollow()}}>{this.state.following? 'UnFollow': 'Follow'}</button>
                        </div>
                    </div>
                ): (null)
                }
            </React.Fragment>

        )
    }

    render () {
        console.log("came into school");
        let statusform = null;
        if (this.state.ismoderator){
            statusform = <StatusUpdateForm
          feedGroup={this.feedgroup}
          userId = { this.feedid }
          doRequest = { this.doupdaterequest}
        />

        }
    return (
        <React.Fragment>
            <div id="react-feed">
            {this.schoolcard()}
            {statusform}
         <FlatFeed
          options={{reactions: { recent: true } }}
          feedGroup = {this.feedgroup}
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
export default SchoolFeed
