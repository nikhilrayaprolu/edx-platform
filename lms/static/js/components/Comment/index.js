import React from 'react';
import { humanizeTimestamp, removeComment } from '../../utils';
import { Dropdown, Link, CommentItem } from 'react-activity-feed';

/**
 * Component is described here.
 *
 * @example ./examples/UserBar.md
 */
export default class Comment extends React.Component {
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
  render() {
      let timestamp = this.props.text.comment.created_at;
      let username = this.props.text.comment.user.data.name;
      let time = humanizeTimestamp(timestamp);
      let comment = this.props.text.comment.data.text;
      const { isLoaded, userid } = this.state;
      let renderData = null;
      if(isLoaded && userid === this.props.text.comment.user_id)
          renderData = (
                <Dropdown>
                    <ul>
                        <li><Link onClick={() => {removeComment(this.props.text.comment.id);}}>Remove</Link></li>
                    </ul>
                </Dropdown>
          );
    return (
      <div className="raf-user-bar">
        <div className="raf-user-bar__details">
            <div id="profileImageIn">{username[0]}</div>
          <p className="raf-user-bar__usernameIn" >
              <strong>{username}</strong> {comment}
          </p>
        </div>
        <React.Fragment>
            <div className="raf-user-bar__extra">
              <time
                dateTime={time}
                title={time}
              >
                {time}
              </time>
                {renderData}
            </div>
         </React.Fragment>
      </div>
    );
  }
}
