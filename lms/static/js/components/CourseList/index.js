import React from 'react';
import CoursesListItem from "../CourseListItem";
export default class CoursesList extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
        apiFetchActive: false,
        coursesData: this.props.coursesData,
    }


  }

  render() {
      let explore = null;
      let buttontext = 'Go to Subject'
    if(this.props.currentcard == 'skills') {
        explore = <p style={{textAlign: 'right', marginTop: '1rem'}}><a href={'/courses'}>Explore More Skills >></a></p>
        buttontext = 'Go to Course'
    }
    if(this.state.coursesData.length == 0){
        return (
            <React.Fragment>
                <div className="section__dash"></div>
                <h1 className="section__title">{this.props.section_title} </h1>
                <div style={{textAlign: 'center'}}>
                <p >You are not subscribed to any skills yet.</p>
                <button type="button"  className="btn btn-primary button-courses" style={{borderRadius: '10px%'}}>Explore Courses</button>
                    </div>
            </React.Fragment>
        )
    }
    return (
      <React.Fragment>
          <div className="section__dash"></div>
          <h1 className="section__title">{this.props.section_title} </h1>
          {this.state.coursesData.map((course => <CoursesListItem courseData={course} buttontext={buttontext}/>))}
          {explore}
      </React.Fragment>
    );
  }
}
