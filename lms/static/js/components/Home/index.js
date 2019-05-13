import React from 'react';
import {
    Activity,
    CommentField, CommentList,
    FlatFeed,
    LikeButton,
    StatusUpdateForm,
    RepostButton,
    AttachedActivity
} from "react-activity-feed";
//import {addReaction} from '../../utils.js';
import {browserHistory} from 'react-router';
import {withRouter} from "react-router-dom";
import UserBar from "../YSUserBar";
import Comment from "../Comment";
class Home extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isLoaded: false,
            userid: ""
        };
    }
    componentDidMount() {
        fetch('/youngwall/me')
            .then(res => res.json())
            .then((result) => {
                this.setState({
                    isLoaded: true,
                    userid: result,
                });
            }, (error) => {
                this.setState({
                    isLoaded: true,
                    userid: ""
                })
            });
    }
    render () {
        const {isLoaded, userid} = this.state;
        if(!isLoaded)
            return <h1>Loading...</h1>;
    return (
        <React.Fragment>
        <StatusUpdateForm
          feedGroup="user"
        />
         <FlatFeed
          options={{reactions: { recent: true } }}
          notify
          Activity={(props) => {
              if(props.activity.verb === "repost") {
                  props.activity.actor = props.activity.actor_temp;
                  props.activity.object = props.activity.object_temp;
                  return (
              <Activity {...props}
                  onClickUser = {(user) => {console.log(user);this.props.history.push(user.id)}}
                    Header={() => (
                                      <UserBar {...props} />
                          )}
                    Content={() => (
                      <AttachedActivity {...props}
                          activity={props.activity.object}
                      />)}
                  Footer={() => (
                      <div style={ {padding: '8px 16px'} }>
                          <LikeButton {...props} />
                  {/* TODO Repost Button
                          <RepostButton
                                activity={props.activity}
                                onToggleReaction={() => {
                                    console.log(props);
                                    //addReaction(userid, props.activity.id, props.activity.origin, props.activity.object);
                                }}
                                userId={userid}
                           /> */}
                          <CommentField
                              activity={props.activity}
                              onAddReaction={props.onAddReaction}
                          />
                          <CommentList
                              activityId={props.activity.id}
                              CommentItem={(text) => (
                                  <Comment text={text}/>
                              )}
                          />
                      </div>
                  )}
              />)
                  }
          return (
              <Activity {...props}
                  onClickUser = {(user) => {console.log(user);this.props.history.push(user.id)}}
                    Header={() => (
                                      <UserBar {...props} />
                          )}
          HeaderRight={() => (
            <Dropdown>
              <div>
                <Link
                  onClick={() => {
                    props.onRemoveActivity(props.activity.id);
                  }}
                >
                  Remove
                </Link>
              </div>
            </Dropdown>
          )}

                  Footer={() => (
                      <div style={ {padding: '8px 16px'} }>
                          <LikeButton {...props} />
                  {/*<RepostButton
                                activity={props.activity}
                                onToggleReaction={() => {
                                    console.log(props);
                                    addReaction(userid, props.activity.id, props.activity.origin, props.activity.object);
                                }}
                                userId=''
                          /> */}
                          <CommentField
                              activity={props.activity}
                              onAddReaction={props.onAddReaction}
                          />
                          <CommentList
                              activityId={props.activity.id}
                              CommentItem={(text) => (
                                  <Comment text={text}/>
                              )}
                          />
                      </div>
                  )}
              />);
          }

          } />
        </React.Fragment>

    )
  }
}
export default withRouter(Home)
