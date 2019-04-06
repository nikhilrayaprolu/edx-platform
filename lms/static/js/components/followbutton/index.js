import React from 'react';

/**
 * Component is described here.
 *
 * @example ./examples/FollowButton.md
 */
export default class FollowButton extends React.Component {
  constructor(props) {
    super(props);
    this.state = { followed: this.props.followed || false };
  }

  render() {
    const { clicked, followed } = this.props;
    return (
      <div
        className={`raf-follow-button ${
          this.state.followed ? 'raf-follow-button--active' : ''
        }`}
        role="button"
        onClick={()=>{clicked(); this.setState({followed: !this.state.followed})}}
      >
        {this.state.followed ? 'Following' : 'Follow'}
      </div>
    );
  }
}
