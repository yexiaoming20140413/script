#!/usr/bin/node
/**
 * Created by linfeiyang on 1/19/16.
 */

var db = require('mysql');
var async = require('async');

var dbconfig = {
    host: '172.16.0.10',
    user: 'root',
    password: 'gozapdev',
    port: 3300,
    database: 'sp2p'
};

var pool = db.createPool(dbconfig);

if(!pool){
    throw new Error('create poll fail');
}
var connection = null;
var ret = '';
async.waterfall([
    function(next){
        pool.getConnection(function (err, conn) {
            if(err) return next(err);
            connection = conn;
            next(null);
        });
    },
    function(next){
        connection.query('select * from t_approve_notice_template', function(err, data){
            if(err) return next(err);
            next(err, data);
        });
    },
    function(data, next){
        console.log(next);
        console.log(data);
        if(data && data.length > 0){
            data.forEach(function(item){
                ret+='public final static String LONGDAI_' + item.nid.toUpperCase() + ' = "' + item.nid + '"; //' +  item.name + '\n';
            });
            next(null);
        } else {
            next(new Error('no data found'));
        }
    }
], function(err){
    if(err) throw err;
    console.log(ret);
});