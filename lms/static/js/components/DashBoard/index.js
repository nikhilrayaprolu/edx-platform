import React from 'react';
import {context} from "../../utils";
import CoursesList from "../CourseList";
import Feed from "../FeedDash";
import UserComponent from "../UserComponentDash";
import LeaderBoard from "../Leaderboard";
import SchoolFeed from "../SchoolDash";
import GroupStats from "../GroupStatsDash";

export default class Dashboard extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            error: null,
            isLoaded: false,
            context: null,
            showsocialwall: null,
            showyoungskills: null,
            showschoolpage: null

        };
        console.log(window.showsocialwall)
        console.log("checking social wall",window.showsocialwall=="False")


    }
    componentWillMount() {
        fetch("/dashboard_api/")
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({
                        isLoaded: true,
                        context: result,
                    });
                },
                (error) => {
                    this.setState({
                        isLoaded: true,
                        error
                    })
                }
            )
        if(window.showsocialwall=="False"){
            this.setState({
                showsocialwall: 'social_wall',
                    });
            console.log(this.state.showsocialwall)
        }

        if(window.showyoungskills=="False")
            this.setState({
                showyoungskills: 'young_skills',
                    });
        if(window.showschoolpage=="False")
            this.setState({
                showschoolpage: 'school_page',
                    });
    }
    render () {
        const { error, isLoaded, context} = this.state;
        return this.state.context && (
            <React.Fragment>
                <div className="container">
                    <div className="row">
                        <div className="col-md-8 card shadow-2" style={{border: '0px'}}>
                            <div className="card-body">
                                <div className="card">
                                    <div className="card-body shadowown">
                                        <CoursesList coursesData={this.state.context['course_enrollments']} section_title={'School Subjects'} currentcard={'subjects'}/>
                                    </div>
                                </div>
                                  <br/>
                                <div className={"card " + this.state.showyoungskills}>
                                    <div className="card-body shadowown">
                                        <CoursesList coursesData={this.state.context['young_skills']} section_title={'Subscribed YoungSkills'} currentcard={'skills'} />
                                    </div>
                                </div>
                                        <br/>
                                <div className={"card " + this.state.showsocialwall}>
                                    <div className="card-body shadowown">
                                        <Feed apiKey={this.state.context.apiKey} appId={this.state.context.appId} social_token={this.state.context.social_token} section_title={'EduSocial Wall'}/>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className="col-md-4 card shadow-2" style={{border: '0px'}}>
                            <div className="card-body">
                                <div className="card">
                                    <div className="card-body shadowown">
                                        <UserComponent youngskill_count={this.state.context.young_skills.length} school_course_count={this.state.context.course_enrollments.length}/>
                                    </div>
                                </div>
                                <br />
                                <div className="card">
                                    <div className="card-body shadowown">
                                        <LeaderBoard user_engagement_score={this.state.context.user_engagement_score} class_average_score={this.state.context.class_average_score} user_position={this.state.context.user_position} leaderboard={this.state.context.leaderboard} />
                                    </div>
                                </div>
                                <br />
                                <div className={"card " + this.state.showschoolpage}>
                                    <div className="card-body shadowown">
                                        <SchoolFeed apiKey={this.state.context.apiKey} appId={this.state.context.appId} social_token={this.state.context.social_token} feedgroup={'school'} feedid={this.state.context.school} section_title={'School Page'}/>
                                    </div>
                                </div>
                                <br />
                                <div className={"card " + this.state.showsocialwall}>
                                    <div className="card-body shadowown">
                                        <GroupStats userid={this.state.context.userid} section_title={'Groups'}/>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                </div>
            </React.Fragment>
        );

    }


}

