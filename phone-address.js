#!/usr/bin/node
/**
 * Created by linfeiyang on 1/7/16.
 */
var mysql = require('mysql');
var async = require('async');
var request = require('request');

var dbconfig = {
    host: '172.16.0.10',
    user: 'root',
    password: 'gozapdev',
    port: 3300,
    database: 'sp2p'
};

var pool = mysql.createPool(dbconfig);
var addressList = [];
var totalCount = 0;
var currPage = -1;
var pageCount = 2000;
var i = 0;
pool.getConnection(function (err, connection) {
    if (err) {
        console.log(err.message);
        return;
    }
    connection.query('SELECT COUNT(1) as `count` FROM t_user', function(err, result){
        if(err) {
            console.log(err.message);
            return ;
        }
        if(result && ~~result[0].count > 0){
            totalCount = ~~result[0].count;
            console.log('total count ' + totalCount);
            async.forever(function(callback){
                currPage++;
                async.waterfall([
                    function (next) {
                        connection.query('SELECT id,mobilePhone FROM t_user LIMIT ' + currPage * pageCount + ',' + pageCount, function (err, users) {
                            next(err, users);
                        });
                    },
                    function (users, next) {
                        if (users && users.length > 0) {
                            next(null, users);
                        } else {
                            callback(new Error('users is empty'));
                        }
                    },
                    function (users, next) {
                        async.eachSeries(users, function (user, next) {
                            console.log(i++ + ',' + totalCount);
                            if (user.hasOwnProperty('mobilePhone') && user['mobilePhone']) {
                                if (user['mobilePhone'].length == 11) {
                                    getPhoneAddress(user['mobilePhone'], function (err, address) {
                                        if (err) {
                                            console.log(err);
                                        } else {
                                            //addressList.push(address);
                                            console.log(address);
                                            addToList(address);
                                        }
                                        next(null);
                                    });
                                } else {
                                    //next(new Error('手机号码长度不正确,ID:' + user.id + ',phone:' + user['mobilePhone']));
                                    console.log('手机号码长度不正确,ID:' + user.id + ',phone:' + user['mobilePhone']);
                                    next(null);
                                }

                            } else {
                                console.log('手机号为空,ID号为' + user.id);
                                next(null);
                            }
                        }, function (err) {
                            next(err);
                        })
                    }
                ], function (err) {
                    callback(null);
                });
            },
            function(err){
                console.log(err);
                console.log(JSON.stringify(addressList));
                process.exit(0); //执行完毕 关闭进程
            });
        } else {
            console.log('error count is error, count:' + result.count);
        }
    });
});

function getPhoneAddress(phone, callback) {
    request.get('http://wap.ip138.com/sim_search138.asp?mobile=' + phone.substr(0, 7), {timeout: 3000}, function (err, result, body) {
        if (err) return callback(err);
        var pattern = /归属地：([^<]+)</;
        var res = body.match(pattern);
        if (res && res.length >= 2) {
            callback(null, res[1].split(' ')[0]);
        } else {
            callback(new Error('get address error, phone:' + phone));
        }
    });
}

function addToList(address) {
    var added = false;
    addressList.forEach(function (item, i) {
        if (!added) {
            if (item.name == address) {
                addressList[i]['count'] = ~~item.count + 1;
                added = true;
            }
        }
    });
    if (!added) {
        addressList.push({name: address, count: 1});
    }
}