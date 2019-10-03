import React, { Component } from 'react';
import { API_KEY, API_URL } from '../../config';
import Navigation from './../elements/Navigation/Navigation';
import MovieInfo from './../elements/MovieInfo/MovieInfo';
import MovieInfoBar from './../elements/MovieInfoBar/MovieInfoBar';
import FourColGrid from './../elements/FourColGrid/FourColGrid';
import Actor from './../elements/Actor/Actor';
import Spinner from './../elements/Spinner/Spinner';
import './Movie.css';



export default class Movie extends Component {
    state = {
        movie: null,
        actors: null,
        directors: [],
        loading:false
        
    }

    componentDidMount() {
        this.setState({
            loading:true,
        })

        const endpoint = `${API_URL}movie/${this.props.match.params.movieId}?api_key=${API_KEY}&language=en-US`;

        this.fetchItems(endpoint);
    }

    fetchItems = (endpoint) => {
        fetch(endpoint).then(result => 
            result.json()
            
        ).then(result => {
            console.log(result);

            if (result.status_code) {
                this.setState({loading:false})
            } else
            {
                this.setState({ movie: result }, () => {
                    const endpoint = `${API_URL}movie/${this.props.match.params.movieId}/credits?api_key=${API_KEY}&language=en-US`;
                    fetch(endpoint).then(result => result.json()).then(result => {
                        console.log('For Actors And DIrectorss'+result);
                        const directors = result.crew.filter(member =>  member.job === 'Director');

                        this.setState({
                            actors: result.cast,
                            directors,
                            loading:false
                        })
                    })
                })
            }
        })

    }

    render() {
        return (
            <div className="rmdb-movie">
                {this.state.movie ? 
                <div>
                        <Navigation movie={this.props.location.movieName} />
                        <MovieInfo movie={this.state.movie} directors={this.state.directors} />
                        <MovieInfoBar time={this.state.movie.runtime} budget={this.state.movie.budget} revenue={this.state.movie.revenue}/>
                        
                </div>
                    : null}
                
                {this.state.actors ?
                    <div className="rmdb-movie-grid">
                        <FourColGrid header={'Actors'}>
                            
                            {this.state.actors.map((element, i) => {return <Actor key={i} actor={element}/>  })}
                              
                        </FourColGrid>
                    </div>
                    : null}
                
                {this.state.actor && !this.state.loading ? <h1>No Movie Found</h1> : null}
                {this.state.loading ? <Spinner/>:null}
            </div>
        )
    }
}
