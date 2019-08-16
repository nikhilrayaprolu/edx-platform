import React from 'react';

export default class LeaderBoard extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            error: null,
            isLoaded: false,
            user_engagement_score: this.props.user_engagement_score,
            class_average_score: this.props.class_average_score,
            user_position: this.props.user_position,
            leaderboard: this.props.leaderboard,


        }
    }


    render() {
        const userlist = (this.state.leaderboard)? this.state.leaderboard.queryset.map((user, i) => <User username={ user.user__username } rank={ i + 1 } img={ "https://cdn2.iconfinder.com/data/icons/budicon-user/16/32-user_-_single-512.png" } score={ user.score } firstname= {user.user__mini_user_profile__first_name} />) : null;

        return (
            <div className="leadercontainer">
                <LeaderboardHeader />
                <ColumnHeader/>
                { userlist }
            </div>
        )
    }
}

const LeaderboardHeader = () => {
  return (
    <div className="leadheader">
        <h2>Leaderboard</h2>
    </div>
  )
}

const ColumnHeader = () => (
  <div className="row colheader">
      <div className="col-md-1">
        <h4>#</h4>
      </div>
      <div className="col-md-5">
        <h4>Name</h4>
      </div>
      <div className="col-md-4">
        <h4 >Score</h4>
      </div>
    </div>
);

const User = ({ rank, img, username, score, firstname}) => {
  return (
    <div className="row users  vcenter">
        <div className="col-md-1 rank">
          <h4>{ rank }</h4>
        </div>
        <div className="col-md-8 name">
          <img src={ img } alt='avatar' /> <a href={`/youngwall/${username}`}  target="_blank">{ firstname }</a>
        </div>
        <div className="col-md-3">
          <h4>{ score }</h4>
        </div>
      </div>
  )
}

