import React from 'react';
import ReactDOM from 'react-dom';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Card from 'react-bootstrap/Card';

import 'bootstrap/dist/css/bootstrap.min.css';
import './index.css';

class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isPlaylistPage: false,
            playlist: [],
            duration: 0
        }
    }

    setIsPlaylistPage = (val, playlistData) => {
        this.setState({isPlaylistPage: val}, () => {
            if (this.state.isPlaylistPage) {
                this.setState({playlist: playlistData.playlist, duration: playlistData.duration});
            } else {
                this.setState({playlist: [], duration: 0});
            }
        })
    }

    helpWindow = () => {
        alert("To use this app, insert individual queries into the input box. To add more queries, click on 'Add Query'. "
            + "You can also define the desired duration for your playlist! After you're done, click on 'Generate Playlist!'"
        );
    }

    render() {
        if (!this.state.isPlaylistPage) {
            return (
                <div>
                    <Button onClick={this.helpWindow} style={{position: "absolute", right: 10, top: 10}}
                            variant="outline-primary">Help!</Button>
                    <PlaylistInputs setIsPlaylistPage={this.setIsPlaylistPage}/>
                </div>
            );
        } else {
            return (
                <Playlist playlist={this.state.playlist} duration={this.state.duration}
                          setIsPlaylistPage={this.setIsPlaylistPage}/>
            )
        }
    }
}

class Playlist extends React.Component {
    // Based on https://stackoverflow.com/questions/37096367/how-to-convert-seconds-to-minutes-and-hours-in-javascript
    secondsToHms = (d) => {
        d = Number(d);
        const h = Math.floor(d / 3600);
        const m = Math.floor(d % 3600 / 60);
        const s = Math.floor(d % 3600 % 60);

        const hDisplay = h > 0 ? h + (h === 1 ? " hour, " : " hours, ") : "";
        const mDisplay = m > 0 ? m + (m === 1 ? " minute, " : " minutes, ") : "";
        const sDisplay = s > 0 ? s + (s === 1 ? " second" : " seconds") : "";
        return hDisplay + mDisplay + sDisplay;
    }

    render() {
        return (
            <div>
                <Button style={{position: "absolute", right: 20, top: 20}}
                        onClick={() => this.props.setIsPlaylistPage(false)}
                        variant="primary">
                    Return to playlist generation
                </Button>
                <div style={{margin: "100px 200px", width: "100%"}}>
                    <span style={{
                        fontSize: 30,
                        backgroundColor: "white"
                    }}>Duration: {this.secondsToHms(this.props.duration)}</span>
                    {
                        this.props.playlist.map((song, i) => {
                            return (
                                <Card key={i} style={{width: '30rem'}}>
                                    <Card.Body>
                                        <Card.Title>{song[0]}</Card.Title>
                                        <Card.Subtitle className="mb-2 text-muted">{song[2]}</Card.Subtitle>
                                        <Card.Text>
                                            {
                                                song[3] === null ? "" : song[3]
                                            }
                                        </Card.Text>
                                    </Card.Body>
                                </Card>
                            )
                        })
                    }
                </div>
            </div>
        )
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
        if (response && response.playlist && response.playlist.length > 0) {
            this.props.setIsPlaylistPage(true, response)
        } else {
            alert("Something went wrong with this query!")
        }
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
            <Form onChange={this.onChange} onSubmit={(event) => event.preventDefault()}>
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

