import React from 'react';
import {context} from "../../utils";

export default class CourseOutline extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            error: null,
            isLoaded: false,
            context: null,
        }
        this.sectiondisplay = this.sectiondisplay.bind(this);
        this.evensubsection = this.evensubsection.bind(this);
        this.oddsubsection = this.oddsubsection.bind(this);
    }
    componentWillMount() {
        fetch("/courses/"+window.course+"/course/outline_api")
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
    }

    evensubsection(subsection1, subsection2, current, prev=0, next=0) {
        let render_items = [];
        if(current == 0) {
            render_items.push(<div className="topic-connector-2"></div>)
        } else {
            render_items.push(<div className="rowyoung">
                                    <div className="topic-vertical-separator"></div>
                                </div>)
        }
        render_items.push(<div className="rowyoung">
                                    <div className="topic-box locked">
                                        <a href={subsection1['lms_web_url']}
                                        >
                                            <div className="topic-icon">
                                                <span className="arrays subject-icon"></span>
                                            </div>
                                            <div className="topic-title">{subsection1['display_name']}</div>
                                        </a>
                                    </div>
                                    <div className="topic-box locked">
                                        <a href={subsection2['lms_web_url']}
                                        >
                                            <div className="topic-icon">
                                                <span className="math subject-icon"></span>
                                            </div>
                                            <div className="topic-title">{subsection2['display_name']}</div>
                                        </a>
                                    </div>
                                </div>)
        return render_items

    }
    oddsubsection(subsection, current, prev=0, next=0) {
        let render_items = []
        if(current == 0) {
            render_items.push(<div className="topic-connector-1"></div>)
        } else {
            render_items.push(<React.Fragment><div className="topic-connector-1"></div>
                                    <div className="topic-vertical-separator"></div></React.Fragment>
                                )
        }
        render_items.push(<div className="topic-box locked">
                                    <a href={subsection['lms_web_url']}
                                    >
                                        <div className="topic-icon">
                                                <span className="math subject-icon"></span>
                                            </div>
                                            <div className="topic-title">{subsection['display_name']}</div>
                                    </a>
                                </div>)
        return render_items


    }
    sectiondisplay(section, index) {
        let subsections = section['children']
        let render_items = []
        if (subsections){
        let subsection_length = subsections.length

        if(index === 0) {
            render_items.push(
                <div className="checpoint-problems">
                                    <a href={section['lms_web_url']}>
                                        <div>
                                            <i className="fa fa-key"></i>{section['display_name']}
                                            <span className="glyphicon glyphicon-info-sign pull-right"
                                                  data-toggle="tooltip" data-placement="right"
                                                  title="Skip problems from previous topics and jump to next level by solving these problems."></span>
                                        </div>
                                    </a>
                                </div>,
                        <div className="topic-vertical-separator"></div>,<div className="level-title">Level {index+1}</div>, <div className="topic-vertical-separator"></div>
                        )

        } else {
            let prevsection = this.state.context["blocks"]["children"][index-1]["children"];
            console.log(prevsection)
            if( prevsection && !(prevsection.length % 2)){
            render_items.push(<div className="topic-connector-2-bottom"></div>,
                                <div className="topic-vertical-separator"></div>,<div className="checpoint-problems">
                                    <a href={section['lms_web_url']}>
                                        <div>
                                            <i className="fa fa-key"></i>{section['display_name']}
                                            <span className="glyphicon glyphicon-info-sign pull-right"
                                                  data-toggle="tooltip" data-placement="right"
                                                  title="Skip problems from previous topics and jump to next level by solving these problems."></span>
                                        </div>
                                    </a>
                                </div>,

                                <div className="topic-vertical-separator"></div>, <div className="level-title">Level {index+1}</div>, <div className="topic-vertical-separator"></div>)
            } else  {
                render_items.push(<div className="topic-connector-1-bottom"></div>,
                                <div className="topic-vertical-separator"></div>,<div className="checpoint-problems">
                                    <a href={section['lms_web_url']}>
                                        <div>
                                            <i className="fa fa-key"></i>{section['display_name']}
                                            <span className="glyphicon glyphicon-info-sign pull-right"
                                                  data-toggle="tooltip" data-placement="right"
                                                  title="Skip problems from previous topics and jump to next level by solving these problems."></span>
                                        </div>
                                    </a>
                                </div>,

                                <div className="topic-vertical-separator"></div>, <div className="level-title">Level {index+1}</div>, <div className="topic-vertical-separator"></div>)

            }

        }
        let prev = 0;
        let next = 0;
        let i = 0
        for(; i < subsection_length-1;) {
            render_items.push(this.evensubsection(subsections[i], subsections[i+1], i));
            i +=2;
        }
        if(i == subsection_length -1) {
            if(i!=0)
                render_items.push(<div className="topic-connector-2-bottom"></div>,this.oddsubsection(subsections[i], i ));
            else
                render_items.push(this.oddsubsection(subsections[i], i ));
        }
        }

        return render_items
    }
    render () {
        const { error, isLoaded, context} = this.state;
        if(this.state.context){
            console.log(this.state.context)
            return (
                <React.Fragment>
                    <div className="containeryoung">
                        <div id="dashboard-ladder-ct">
                            <div className="dashboard-topics">
                                <div className="rowyoung course-level">
                                    {this.state.context["blocks"]["children"].map((value, index) => {
                                        return this.sectiondisplay(value, index)
                                    })}
                                </div>
                            </div>
                        </div>
                    </div>
                </React.Fragment>
    );
        }

        return null;
    }

    }
