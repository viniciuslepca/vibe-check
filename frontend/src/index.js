import React from 'react';
import ReactDOM from 'react-dom';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';

import 'bootstrap/dist/css/bootstrap.min.css';
import './index.css';

class App extends React.Component {
    render() {
        return (
            <div>
                <Button style={{position: "absolute", right: 10, top: 10}} variant="outline-primary">Help!</Button>
                <PlaylistInputs/>
            </div>
        );
    }
}

class PlaylistInputs extends React.Component {
    render() {
        const leftWidth = 5;
        const rightWidth = 12 - leftWidth;
        const whiteTextStyle = {
            fontSize: 30,
            color: "white",
            float: "right",
            marginRight: 5
        }

        const standardMargin = 50;
        return (
            <Container fluid style={{marginTop: 300}}>
                <Row style={{marginBottom: standardMargin}}>
                    <Col xs={leftWidth}>
                        <span style={whiteTextStyle}>Make a playlist with songs...</span>
                    </Col>
                    <Col xs={rightWidth}>
                        <InputQueries/>
                    </Col>
                </Row>
                <Row style={{marginBottom: standardMargin}}>
                    <Col xs={leftWidth}>
                        <span style={whiteTextStyle}>I want my playlist to last</span>
                    </Col>
                    <Col xs={rightWidth}>
                        <TimeQuery/>
                    </Col>
                </Row>
                <Row style={{marginBottom: 20, marginRight: 20, float: "right"}}>
                    <Button variant="primary">Generate Playlist!</Button>
                </Row>
            </Container>
        );
    }
}

class TimeQuery extends React.Component {
    render() {
        const fontSize = 22;
        return (
            <Form>
                <Form.Row>
                    <Col>
                        <Form.Group controlId={"hoursQuery"} style={{marginBottom: 0}}>
                            <Form.Control size="lg" type="number" min={0} defaultValue={0}/>
                        </Form.Group>
                        <span style={{fontSize: fontSize, float: "right"}}>hours</span>
                    </Col>
                    <Col>
                        <Form.Group controlId={"minutesQuery"} style={{marginBottom: 0}}>
                            <Form.Control size="lg" type="number" min={0} defaultValue={30}/>
                        </Form.Group>
                        <span style={{fontSize: fontSize, float: "right"}}>minutes</span>
                    </Col>
                </Form.Row>
            </Form>
        );
    }
}

class InputQueries extends React.Component {
    constructor(props) {
        super(props);
        const exampleQueries = [
            "like Watermelon Sugar",
            "similar to Pink Floyd",
            "from the 80s",
            "by U2",
            "of genre rock",
            "not from the 2010s"
        ]
        this.state = {
            numQueries: 1,
            exampleQueries: exampleQueries
        }
    }

    incrementNumQueries = () => {
        this.setState({numQueries: this.state.numQueries + 1})
    }

    resetQueries = () => {
        this.setState({numQueries: 1})
    }

    render() {
        return (
            <Form>
                {
                    [...Array(this.state.numQueries)].map((_, i) => {
                        return (
                            <Form.Group key={i} controlId={"query" + i}>
                                <Form.Control size="lg" type="text"
                                              placeholder={this.state.exampleQueries[i % (this.state.exampleQueries.length)]}/>
                            </Form.Group>
                        );
                    })
                }
                <Button variant="primary" onClick={this.incrementNumQueries}>Add Query</Button>{' '}
                <Button variant="outline-primary" onClick={this.resetQueries}>Reset Queries</Button>
            </Form>
        );
    }
}

ReactDOM.render(<App/>, document.getElementById('root'));

