#!/usr/local/bin/node
/**
 * Created by linfeiyang on 1/19/16.
 */
var md5 = require("blueimp-md5");

var db = require('mysql');
var async = require('async');
var moment = require('moment');

var dodbconfig = {
    host: '172.16.0.10',
    user: 'root',
    password: 'gozapdev',
    port: 3300,
    database: 'sp2p'
};

var wwdbconfig = {
    host: '192.168.2.114',
    user: 'myviewol',
    password: 'dg2_15@br',
    port: 3330,
    database: 'sp2p'
};

//var pool = db.createPool(dodbconfig);
var pool = db.createPool(wwdbconfig);
if (!pool) {
    throw new Error('create poll fail');
}
var connection = null;

function add_share_red_reward(phone, callback) {
    var userId = '';
    var ret = '';
    async.waterfall([
            function (next) {
                pool.getConnection(function (err, conn) {
                    if (err) return next(err);
                    connection = conn;
                    next(null);
                });
            },
            function (next) {
                var sql = 'select id from t_user where mobilePhone=?';
                connection.query(sql, phone, function (err, data) {
                    if (err) return next(err);
                    if(data && data.length > 0){
                        userId = data[0].id;
                        next(err, userId);
                    } else {
                        next(new Error('没有找到此用户'));
                    }

                });
            },
            function (userId, next) {
                var sql = 'select id,investTime from t_invest where investor = ? order by investTime desc limit 3';
                connection.query(sql, userId, function (err, data) {
                    if(err) return next(err);
                    if(data && data.length > 0){
                        data.forEach(function(item){
                            ret+=userId + ' ' + item.id + ' ' + moment(item.investTime).format('YYYY-MM-DD') + '\n';
                        });
                        next();
                    } else {
                        next(new Error("没有找到数据"));
                    }
                });
            }
        ],
        function (err) {
            if (connection) connection.release();
            if (err) callback(err);
            callback(null, ret);
        });
}


function run() {
    async.eachSeries(process.argv.slice(2), function(item, next){
        add_share_red_reward(item, function(err, res){
            if(err) throw err;
            console.log(res);
            next();
        });
    },function(err){
        if(err) throw err;
        process.exit(0);
    });

}

run();