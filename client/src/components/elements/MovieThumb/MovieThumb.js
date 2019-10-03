import React from 'react';
import './MovieThumb.css';
import { Link } from 'react-router-dom';
export default function MovieThumb(props) {
    return (
        <div className="rmdb-moviethumb">
            <div>
                {props.clickable?<Link to={{pathname:`/${props.movieId}`,movieName: `${props.movieName}`}}> <img className="" src={props.image} alt = "" /></Link>
                 : <img className="" src={props.image} alt = "" />
                 }
               
            </div>
            <p className="form-control" style={{ alignText: 'center', alignItems: 'center', alignContent:'center'}}>{props.movieName}</p>
        </div>
    )
}
