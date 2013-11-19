#ifndef BASE_ICE
#define BASE_ICE

module Trade
{
	//登录时用到的标识
	struct Identity
	{
		string  strName;			//接口访问方的名称
		string	strAccessToken;		//接口访问方提供的token
		string	ptsdid;				
		string 	ptaccount;			//用户pt账号
        string	characterid;		//用户角色id
        string  charactername;		//用户角色名
		string  matrixid;			//用户所在的区组
		string	clientIP;			//用户的请求IP
		string	group;
	};
	
};

#endif