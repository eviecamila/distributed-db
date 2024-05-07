TYPE=TRIGGERS
triggers='CREATE DEFINER=`admindb`@`%` TRIGGER `cdrTrigger` AFTER INSERT ON `cdr` FOR EACH ROW BEGIN\n					INSERT INTO replicate_cdr(calldate, clid, src, dst, dcontext, channel, dstchannel, lastapp, lastdata, duration, billsec, disposition, amaflags, accountcode, uniqueid, userfield, did, recordingfile, cnum, cnam, outbound_cnum, outbound_cnam, dst_cnam, linkedid, peeraccount, sequence) values (new.calldate, new.clid, new.src, new.dst, new.dcontext, new.channel, new.dstchannel, new.lastapp, new.lastdata, new.duration, new.billsec, new.disposition, new.amaflags, new.accountcode, new.uniqueid, new.userfield, new.did, new.recordingfile, new.cnum, new.cnam, new.outbound_cnum, new.outbound_cnam, new.dst_cnam, new.linkedid, new.peeraccount, new.sequence);\n				END'
sql_modes=1411383296
definers='admindb@%'
client_cs_names='utf8mb4'
connection_cl_names='utf8mb4_general_ci'
db_cl_names='latin1_swedish_ci'
created=1713647213963244
