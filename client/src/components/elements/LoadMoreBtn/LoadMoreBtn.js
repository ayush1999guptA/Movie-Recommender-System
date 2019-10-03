import React from 'react';
import './LoadMoreBtn.css';

export default function LoadMoreBtn(props) {
    return (
        <div className="rmdb-loadmorebtn" onClick={props.onClick}>
            <p>{props.text}</p>
           
        </div>
    )
}
