const express = require('express');
const mysql = require('mysql');
const app = express();

app.set('port', 3000);

app.use((req, res, next) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    res.setHeader('Access-Control-Allow-Methods', 'GET,PUT,PATCH,POST,DELETE');
    res.setHeader('Cache-Control', 'no-cache');
    next();
});

app.get('/edinburgh/avg-price-by-neighbourhood-cleansed', (req, res) => {
    var con = mysql.createConnection({
        host: "localhost",
        port: 3306,
        user: "root",
        password: "",
        database: "pract1"
    });
    con.connect(err => {
        if (err) {
            res.status(500).send();
            return;
        }
    });
    con.query(`SELECT geolocation.neighbourhood_cleansed, AVG(listing.price) as avg_price ` +
                `FROM geolocation ` +
                `JOIN listing ON geolocation.id_listing = listing.id ` +
                `WHERE geolocation.municipality = "edinburgh" ` +
                `GROUP BY geolocation.neighbourhood_cleansed`, (err, result) => {
        if (err) throw err;
        res.json(result);
    });
    con.end(err => {
        if (err) throw err;
    });
});

app.get('/edinburgh/avg-reviews-by-neighbourhood-cleansed', (req, res) => {
    var con = mysql.createConnection({
        host: "localhost",
        port: 3306,
        user: "root",
        password: "",
        database: "pract1"
    });
    con.connect(err => {
        if (err) {
            res.status(500).send();
            return;
        }
    });
    con.query(`SELECT geolocation.neighbourhood_cleansed, AVG(reviews.review_scores_value) as avg_review_scores_value ` +
                `FROM geolocation ` +
                `JOIN reviews ON geolocation.id_listing = reviews.id_listing ` +
                `WHERE geolocation.municipality = "edinburgh" ` +
                `GROUP BY geolocation.neighbourhood_cleansed`, (err, result) => {
        if (err) throw err;
        res.json(result);
    });
    con.end(err => {
        if (err) throw err;
    });
});

app.get('/edinburgh/coordinates-by-listing', (req, res) => {
    var con = mysql.createConnection({
        host: "localhost",
        port: 3306,
        user: "root",
        password: "",
        database: "pract1"
    });
    con.connect(err => {
        if (err) {
            res.status(500).send();
            return;
        }
    });
    con.query(`SELECT latitude, longitude ` +
                `FROM geolocation ` +
                `JOIN listing ON geolocation.id_listing = listing.id ` +
                `WHERE geolocation.municipality = 'edinburgh'`, (err, result) => {
        if (err) throw err;
        res.json(result);
    });
    con.end(err => {
        if (err) throw err;
    });
});

app.get('/santiago/avg-price-by-neighbourhood-cleansed', (req, res) => {
    var con = mysql.createConnection({
        host: "localhost",
        port: 3306,
        user: "root",
        password: "",
        database: "pract1"
    });
    con.connect(err => {
        if (err) {
            res.status(500).send();
            return;
        }
    });
    con.query(`SELECT geolocation.neighbourhood_cleansed, AVG(listing.price) as avg_price ` +
                `FROM geolocation ` +
                `JOIN listing ON geolocation.id_listing = listing.id ` +
                `WHERE geolocation.municipality = "santiago" ` +
                `GROUP BY geolocation.neighbourhood_cleansed`, (err, result) => {
        if (err) throw err;
        res.json(result);
    });
    con.end(err => {
        if (err) throw err;
    });
});

app.get('/santiago/avg-reviews-by-neighbourhood-cleansed', (req, res) => {
    var con = mysql.createConnection({
        host: "localhost",
        port: 3306,
        user: "root",
        password: "",
        database: "pract1"
    });
    con.connect(err => {
        if (err) {
            res.status(500).send();
            return;
        }
    });
    con.query(`SELECT geolocation.neighbourhood_cleansed, AVG(reviews.review_scores_value) as avg_review_scores_value ` +
                `FROM geolocation ` +
                `JOIN reviews ON geolocation.id_listing = reviews.id_listing ` +
                `WHERE geolocation.municipality = "santiago" ` +
                `GROUP BY geolocation.neighbourhood_cleansed`, (err, result) => {
        if (err) throw err;
        res.json(result);
    });
    con.end(err => {
        if (err) throw err;
    });
});

app.listen(app.get('port'), () => {
    console.log('Server started: http://localhost:' + app.get('port') + '/');
});
