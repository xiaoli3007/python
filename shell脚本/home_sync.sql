INSERT INTO `home`.`fg_member` 
 (userid,phpssouid,username,password,encrypt,nickname,setting,avatar,upload_size,used_size,export_id,status) 
SELECT userid,phpssouid,username,password,encrypt,nickname,setting,avatar,upload_size,used_size,export_id,status FROM 
 `train`.`v9_member` as a  WHERE NOT EXISTS(SELECT userid FROM `home`.`fg_member`  as b
where a.userid = b.userid);

