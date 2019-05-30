import React from 'react';
import {Button} from "react-activity-feed";
export default class RedirectTimeline extends React.Component {
    constructor(props) {
    super(props);
    this.onClick = this.onClick.bind(this);
  }
    onClick() {
        this.props.history.push('/youngwall')
    }
    render() {
        let button = null
        if(!this.props.schoolpage)
            button = <div className="raf-load-more-button">
                <a href={'/youngwall/'}>
                    <Button
                        buttonStyle="info"
                    >
                        Go to TimeLine to see more posts
                    </Button>
                </a>
                </div>
        return (
            <React.Fragment>
                {!this.props.reverse && this.props.children}
                {button}
        {this.props.reverse && this.props.children}

            </React.Fragment>
        );
    }
}
