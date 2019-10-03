import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Home from '../Home/Home';
import Header from '../elements/Header/Header';
import NotFound from './../elements/NotFound/NotFound';
import Movie from './../Movie/Movie';

const App = () => {
    return (
        <div>
            {/* 
            <Home/> */}
            <Router>
                <React.Fragment>
                    <Header />
                    
                    <Switch>
                        <Route exact path="/" component={Home} />
                        <Route exact path="/:movieId" component={Movie} />
                        <Route component={NotFound} />
                    </Switch>   
                </React.Fragment>
                


            </Router>
                
        </div>
    )
}
export default App;

