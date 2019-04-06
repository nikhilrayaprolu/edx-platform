import React from 'react';
import {
    Activity,
    CommentField, CommentList,
    FlatFeed,
    LikeButton,
    StatusUpdateForm,
} from "react-activity-feed";
import UnApprovedGroup from "../UnApprovedGroup";
import SchoolGroup from "../SchoolGroup";
import {doupdaterequest, feedrequest, getCookie, handlefollow} from "../../utils";
import UserBar from "../YSUserBar";
class Group extends React.Component {
    constructor(props) {
        super(props);
        this.doupdaterequest = this.doupdaterequest.bind(this);
        this.state = {
            error: null,
            isLoaded: false,
            ismoderator: false,
            user_profile: null,
            globalgroup: true,
            group_details: null,
            following: false,
        };
        this.feedid = this.props.match.params.groupid;
        this.feedgroup = 'globalgroup';
        this.unapprovedfeedgroup = 'unapprovedgroup'
        this.togglesubgroup = this.togglesubgroup.bind(this);
        this.handlefollow = this.handlefollow.bind(this);
        this.navigationbar = this.navigationbar.bind(this);

    }
    componentWillMount() {
        var csrftoken = getCookie('csrftoken');
        fetch("/youngwall/moderator/"+this.props.match.params.groupid)
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({
                        isLoaded: true,
                        ismoderator: result.ismoderator,
                        user_profile: result.user_profile,
                        globalgroup: true,
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
        if(this.state.ismoderator){
            doupdaterequest(params, this.feedgroup, this.feedid)
        } else {
            doupdaterequest(params, this.unapprovedfeedgroup, this.feedid)
        }

    }

    togglesubgroup() {
        this.setState(prevstate => (
            {   ...prevstate,
                globalgroup: !prevstate.globalgroup,

            }
        ), () => {
            console.log(this.state.globalgroup)
        })
    }
    handlefollow(id) {
        handlefollow(this.state.user_profile.page_id, this.feedid, 'globalgroup');
        this.setState(prevstate => ({ ...prevstate, following: !prevstate.following }))

    }

    navigationbar(activegroup) {
        return (
            <ul className="nav nav-pills">
                <li className="nav-item">
                    <button className={'nav-link ' + ((activegroup == 'globalgroup')? 'active': '')} onClick={this.togglesubgroup}>Global Group</button>
                </li>
                <li className="nav-item">
                    <button className={'nav-link ' + ((activegroup == 'schoolgroup')? 'active': '')} onClick={this.togglesubgroup}>School Group</button>
                </li>
            </ul>
        )

    }
    globalgroupfeed() {
        let unapprovedposts = null;
        if(this.state.ismoderator){
            unapprovedposts = <UnApprovedGroup groupid={this.props.match.params.groupid} />
        }
        return (
            <React.Fragment>
                <div id="react-feed">
                    {this.navigationbar(this.feedgroup)}
                    <StatusUpdateForm
                        feedGroup={this.feedgroup}
                        userId = { this.feedid }
                        doRequest = { this.doupdaterequest}
                    />
                    {unapprovedposts}
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
    schoolgroupfeed() {
        return (
            this.state.user_profile && <React.Fragment>
                <div id="react-feed">
                    {this.navigationbar('schoolgroup')}
                    <SchoolGroup schoolgroupid={this.state.user_profile.school + '_' + this.feedid} />
                </div>
            </React.Fragment>
        )
    }
    groupcard() {
        return (
            <React.Fragment>
                { this.state.group_details ? (
                    <div className="card ys-card">
                        <img className="card-img-top ys-group-card-img-top" src="http://www.gstatic.com/tv/thumb/persons/1083/1083_v9_ba.jpg" alt="Card image cap" />
                        <div className="card-body">
                            <h5 className="card-title">{this.state.group_details.name}</h5>
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
        let activecomponent = null;
        if(this.state.globalgroup) {
            activecomponent = this.globalgroupfeed()

        } else {
            activecomponent = this.schoolgroupfeed()
        }
        return (
            <React.Fragment>
                {this.groupcard()}
                {activecomponent}
            </React.Fragment>
        )
    }
}
export default Group
