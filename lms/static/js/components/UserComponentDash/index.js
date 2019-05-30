import React from 'react';

export default class UserComponent extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            error: null,
            isLoaded: false,
            username: '',
            firstname: '',
            email: '',
            followers: '',
            following: '',
            youngskill_count: this.props.youngskill_count,
            school_course_count: this.props.school_course_count,

        }


    }
    componentDidMount() {
        fetch("/youngwall/follow_count")
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({
                        isLoaded: true,
                        username: result.username,
                        firstname: result.first_name,
                        email: result.email,
                        followers: result.followers,
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

    render() {

        return (
            <React.Fragment>
                <div className="card">
                    <img className="card-img-top" src={"https://image.flaticon.com/icons/png/512/64/64572.png"} alt={"Card image cap"} style={{height: '10em', width: '10em',display: 'block',margin: 'auto'}}/>
                        <div className="card-body">
                            <h3 className="card-title">Hi {this.state.firstname}!</h3>
                            <p className="card-text">Username: {this.state.username}</p>
                            <p className="card-text">Email: {this.state.email}</p>
                            <p className="card-text">Followers: {this.state.followers} <a href="/youngwall/myfollowers">list</a></p>
                            <p className="card-text">Following: {this.state.following} <a href="/youngwall/friends">list</a></p>
                            <p className="card-text">YoungSkill Courses: {this.state.youngskill_count}</p>
                            <p className="card-text">School Subjects: {this.state.school_course_count}</p>
                        </div>
                </div>

            </React.Fragment>
        );
    }
}
