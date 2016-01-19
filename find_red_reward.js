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

/*var pool = db.createPool(dodbconfig);*/
var pool = db.createPool(wwdbconfig);
if(!pool){
    throw new Error('create poll fail');
}

var connection = null;
function getRewardUrl(phone, callback){
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
            var sql = 'select a.id,a.createTime,a.userId,b.mobilePhone from t_share_red_reward a left join ' +
                't_user b on a.userId=b.id where mobilePhone= \'' + phone +  '\' order by id desc limit 0,6';
            connection.query(sql, function(err, data){
                if(err) return next(err);
                next(err, data);
            });
        },
        function(data, next){
            if(data && data.length > 0){
                data.forEach(function(item){
                    ret+= 'http://m.longdai.com/shareRedReward?shareRed=' + redHash(item.id) + '\t'
                        + moment(item['createTime']).format('YYYY-MM-DD HH:mm:ss') + '\n';
                });
                next(null);
            } else {
                next(new Error('no data found'));
            }
        }
    ],
    function(err){
        if(connection) connection.release();
        if(err) callback(err);
        callback(null, ret);
    });
}

function redHash(shareId){
    var tmp = parseInt(shareId).toString(3);
    var hash = md5(tmp);
    return (hash + '').toUpperCase();
}

async.eachSeries(process.argv.slice(2), function(item, next){
    if(item && (item + '').match(/\d{11}/)){
        getRewardUrl(item, function(err, result){
            if(err) return next(err);
            console.log(item);
            console.log(result);
            next();
        });
    } else {
        console.log('no vaild phone' + item);
        next(null);
    }
}, function(err){
    if(err) throw err;
    process.exit(0);
});