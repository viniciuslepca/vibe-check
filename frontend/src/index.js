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
    constructor(props) {
        super(props);
        const defaultQuery = "like Watermelon Sugar";
        const defaultTimeMinutes = 30;
        this.state = {
            inputQueries: [defaultQuery],
            defaultQuery: defaultQuery,
            defaultTimeMinutes: defaultTimeMinutes,
            timeInput: [0, defaultTimeMinutes] // [hours, minutes]
        }
    }

    setInputQueries = (queries) => {
        this.setState({inputQueries: queries});
    }

    resetInputQueries = () => {
        this.setState({inputQueries: [this.state.defaultQuery]});
    }

    setTimeInput = (time) => {
        this.setState({timeInput: time})
    }

    generatePlaylist = async () => {
        const timeInput = this.state.timeInput;
        const timeInSeconds = 3600 * timeInput[0] + 60 * timeInput[1];
        const params = {
            duration: timeInSeconds,
            queries: this.state.inputQueries
        }
        const response = await fetch("http://localhost:5000/playlists", {
            method: 'POST',
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(params)
        }).then(response => response.json());
        console.log(response);
    }

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
                        <InputQueries setInputQueries={this.setInputQueries}
                                      resetInputQueries={this.resetInputQueries}
                                      inputQueries={this.state.inputQueries}
                                      defaultQuery={this.state.defaultQuery}/>
                    </Col>
                </Row>
                <Row style={{marginBottom: standardMargin}}>
                    <Col xs={leftWidth}>
                        <span style={whiteTextStyle}>I want my playlist to last</span>
                    </Col>
                    <Col xs={rightWidth}>
                        <TimeQuery timeInput={this.state.timeInput}
                                   defaultTimeMinutes={this.state.defaultTimeMinutes}
                                   setTimeInput={this.setTimeInput}/>
                    </Col>
                </Row>
                <Row style={{marginBottom: 20, marginRight: 20, float: "right"}}>
                    <Button variant="primary" onClick={this.generatePlaylist}>Generate Playlist!</Button>
                </Row>
            </Container>
        );
    }
}

class TimeQuery extends React.Component {
    onChange = (event) => {
        const target = event.target;
        const id = target.id;
        const value = target.value;
        const newTimeInput = this.props.timeInput;
        if (id === "hoursQuery") {
            newTimeInput[0] = value;
        } else if (id === "minutesQuery") {
            newTimeInput[1] = value;
        }
        this.props.setTimeInput(newTimeInput);
    }

    render() {
        const fontSize = 22;
        return (
            <Form onChange={this.onChange} onSubmit={(event) => event.preventDefault()} >
                <Form.Row>
                    <Col>
                        <Form.Group controlId={"hoursQuery"} style={{marginBottom: 0}}>
                            <Form.Control size="lg" type="number" min={0} defaultValue={0}/>
                        </Form.Group>
                        <span style={{fontSize: fontSize, float: "right"}}>hours</span>
                    </Col>
                    <Col>
                        <Form.Group controlId={"minutesQuery"} style={{marginBottom: 0}}>
                            <Form.Control size="lg" type="number" min={0} defaultValue={this.props.defaultTimeMinutes}/>
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
            this.props.defaultQuery,
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
        this.setState({numQueries: this.state.numQueries + 1});
        const newInputQueries = this.props.inputQueries;
        newInputQueries.push("");
        this.props.setInputQueries(newInputQueries);
    }

    resetQueries = () => {
        this.setState({numQueries: 1})
        const value = document.getElementById("query0").value;
        this.props.setInputQueries([value]);
    }

    onBlur = (event) => {
       const target = event.target;
       if (target.tagName.toLowerCase() === "input") {
           const value = target.value;
           const index = target.id.split("query")[1]
           const newInputQueries = this.props.inputQueries;
           newInputQueries[index] = value;
           this.props.setInputQueries(newInputQueries);
       }
    }

    render() {
        return (
            <Form onBlur={this.onBlur} onSubmit={(event) => event.preventDefault()}>
                {
                    [...Array(this.state.numQueries)].map((_, i) => {
                        return (
                            <Form.Group key={i} controlId={"query" + i}>
                                <Form.Control size="lg" type="text" required
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

