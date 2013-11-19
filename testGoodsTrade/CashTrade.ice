#ifndef CASH_TRADE_ICE
#define CASH_TRADE_ICE
#include "base.ice"

module Trade
{
    //卖方信息
    struct Seller
    {
		string 	ptaccount;		//卖方的pt账号
		string	ptsdid;
        string	characterid;	//卖方的角色id
        string  charactername;	//卖方的角色名
		string  matrixid;		//卖方所在的区组
		string  midaccount;     //现金支付中间商户号
    };
    
    //道具信息
    struct Item
    {
        string      bookid;
        string      itemName;
        string      itemImage;
        int			itemId;
        int			itemType;
		float	    price;				//出售的价格
		int			count;				//道具数量
		int			cointype;			//货币类型  1:现金 2:点券
		double	    feeRate;			//费率
		int			feeType;			//买家付费/卖家付费
		double      feeAdd;				//费率加项
		string		couponType;         //使用优惠券类型,如果为空表示不使用优惠券
		int			batches;			//批数，商品以一批为单位进行定价
		int			srcCode;			//订单来源
    };
   
    //角色登录交易中心的相关信息
    struct LoginInfo
    {
		int			gameid;
		int			areaid;
		int			groupid;
		long		characterid;
		string      charactername;
		long		sdid;
		string		ptaccount;
		string		guid;
		string		ip;
		string		redirect;
		int			playid;
		short		level;
		short		sex;
		long		career;
		int			logintime;
    };
    
    struct OrderInfo
    {
		int			nBuyType;
		int			nOrderType;
		int			nStatus;
		string		strKeyword;
		int			nGoodstype;
		int			nStarttime;
		int			nEndtime;
		
    };
    
    struct AddrInfo
    {
		string	strName;
		string	strPhone;
		string	strAddress;
		string	strPostcode;
    };
    
    struct SmRoleInfo
    {
		int			gameid;
		int			areaid;
		int			groupid;
		string		characterid;
		string      charactername;
		string		account;
		int			looks;
		int			career;
		int			pvehp;
		int			pveattack;
		int			pvedefense;
		int			coin;
		int			giftcoin;
		int			gem;
		int			cachegem;
		int			vote;
		int			point;
		int			wooolpoint;
		int			wooolreward;
		int			eyesight;
		int			successivecount;
		int			refreshcount;
		int			state;
		int			skill;
		int			skills;
		int			lastdroptype;
    };
    
    struct SmSkillInfo
    {
		int			id;
		string		name;
		int			model;
		string		color;
		int			coefficient;
		int			career;
		string		url;
		string		memo;
    };
   
    dictionary<string,string> KV;

    interface CashTrade
    {
		//物品下架
		int ItemOffShelf(Identity id, string bookId,int productType);
		
		//更改物品价格
		int ItemUpdatePrice(Identity id, string bookId,string newPrice);
    
		//通知已退款
		int OrderStatusChangeNotify(Identity id,string json);
		
        //购买道具，返回订单信息。
        int BuyItem(Identity id,Seller s,Item i,out string result);									
        
        //购买b2c道具，返回订单信息。
        int BuyB2CItem(Identity id,Seller s,Item i,out string result);
        int RegisterB2CAddress(Identity id,string orderId,AddrInfo info);
        
        //龙之谷团购记录
        int GrouponBuy(Identity id,int groupId,string orderId,string price,int num,int state,out string result);
        
        //抽奖
        int BuyLottery(Identity id,out string result);
        int ShowRecentLotteryResult(Identity id,int page,int count,out string result);
        int	CheckWinLottery(Identity id,string type,out string result);
        int RegisterLotteryAddress(Identity id,AddrInfo info);
        int	ShowMyLotteryResult(Identity id,int page,int count,out string result);
        
        //拉霸
        int AddRole(Identity id, int looks, int career, out string characterInfo);
        int GetRole(Identity id, out string characterInfo);
        int AddCoin(Identity id, int coin);
        int SubCoin(Identity id, int coin);
        int GetCoin(Identity id, out string coinInfo);
        int BuyCoin(Identity id, int coin, out string coinInfo);
        int BuySkill(Identity id, out string skillInfo);
        int ChangeSkill(Identity id, int skill, out string skillInfo);
        int BuyAttr(Identity id, out string characterInfo);
        int BuyLoot(Identity id, int lootId, out string lootInfo);
        
        int GetLastPveBattleScene(Identity id, out string sceneInfo);
        int CalPveResult(Identity id, int select, out string sceneInfo);
        int RefreshPveBattleScene(Identity id, string battleId, out string sceneInfo);
        int UpdateEyeSight(Identity id, int eyeSight, out string sceneInfo);
        int LosingBattle(Identity id, int state);
        
        //拉霸后台配置
        int GetAllSlotMachineConfigs(out string configs);
        int SetSlotMachineConfig(string key, string value);
        int GetMonstersInfo(int page, int count, out string monsters);
        int SetMonsterInfo(int monsterId, string monsterName, int hp, int attack, int defense, string monsterPic);
        int GetPveBattleInfo(string account, int page, int count, out string battleInfo);
        int GetRoleInfo(string account, out string characterInfo);
        int SetRoleInfo(SmRoleInfo info);
        int GetLoots(string lootName, int page, int count, out string lootsInfo);
        int SetLootGoods(int lootId, int lootType, int goodsId, int goodsType, string lootName, string goodsName, string goodsUrl, int goodsCount, int rate);
        int DelLootGoods(int lootId, int goodsId, int goodsType);
        int GetSkillInfo(string skillName, int page, int count, out string skillInfo);
        int SetSkillInfo(SmSkillInfo info);
        int GetCoinLog(string account, int page, int count, out string coinLog);
        
        
        //列出道具,通过type来区分我购买的、我出售的、已下架的等,order_type区分元宝支付还是现金支付。
        int QueryOrderList(Identity id,int type,int orderType,int status,string keyword,int goodsType,int starttime,int endtime,int count,int page,out string result);		
        int QuerySdptOrderList(Identity id,OrderInfo info,int count,int page,out string result);
        
        //拒绝退款申请
        int RefuseRefundApply(Identity id,string orderid,string detail);	
        
        //退款
        int Refund(Identity id,string orderid,string detail);

        //付款结果通知								
		int PayResultNotify(Identity id,string orderid,string sequenceid,bool bSuccess);	
			
		//关闭订单
		int CloseOrder(Identity id,string orderid,int reason,string detail);
			
		//查询多个订单状态，以逗号分割
		int QueryOrderStatus(Identity id,string orderlist,out string result);
			
		//根据订单id查询订单详情
		int QueryOrderDetail(Identity id,string orderid,out string result);
			
		//根据BookId查询订单Id
		int QueryOrderIdByBookId(Identity id,string bookid,out string orderid);
			
		//由于某种原因锁定订单
		int LockOrder(Identity id,string orderid,int reason,string detail);
			
		//解锁订单
		int UnlockOrder(Identity id,string orderid,int reason,string detail);

        //登陆纪录
        int Login(Identity id);
		
		//获取手续费 
		//type 0:买家手续费 1:卖家手续费
		int GetFee(Identity id,string totalPrice, int type,out string fee);
        
        //购买格子铺
        int BuyBag(Identity id, int bagType, int renew,out string result);

        //列出可售包裹
        int ListSellableBag(Identity id,out string baginfo);		
		
		//消息接口
		int GetMessage(Identity id,int isRead,int page,int count, out string result);
		int QueryMessageCount(Identity id,int isRead,out string result);
		int SetMessageStatus(Identity id,string msgId,int status);
		int SendMessage(Identity id,int type,string bookId,string goodsName);
		
		//前端监控脚本
		int Monitor(Identity id,string orderId);
		
		//查询付款状态
		int QueryBillingStatus(Identity id,string orderId,out string result);		
		
		int Lottery(Identity id,int times,int sdptTimes,out string result);
		int QueryLottery(Identity id,out string result);
		int UserCouponList(Identity id, string type,bool isOutDated,int state,int page,int count, out string result);

		//发优惠券,登陆时调用
		//发送优惠券成功返回0
		//其他返回 -1
		int SendCoupon(Identity id);
		
		//列出最近成交的订单
		int ListRecentOrder(Identity id,int count,int type,out string result);		
		
		//处理订单,用于帐号交易服务的被动模式
		//status
		//1 处理初始化订单
		//2 处理待支付订单
		//4 处理付款通知的订单
		//5 处理确认付款的订单
		//7 处理转移物品成功的订单
		//8 处理超时未支付订单
		//32 处理确认购买帐号的订单
		
		int ProcessOrders(Identity id,int status, out string result);
		//获取确认购买帐号的手机验证码
		int GetConfirmBuyAccountVerifyKey(Identity id,KV paramlist);
		//确认购买帐号
		int ConfirmBuyAccount(Identity id,KV paramlist, out string result);
		//获取帐号临时密码
		int GetAccountTempPass(Identity id,string orderId,out string result);
        //购买帐号，返回订单信息。
        int BuyAccount(Identity id,KV paramlist,out string result);	
        
        //退款申请,帐号交易
        int RefundApply(Identity id,KV paramlist,out string result);
        //判定购买，由后台调用
        int JugeTrade(Identity id,KV paramlist,out string result);	 
        
        //通用hps接口
		int RequestApi(Identity id,string method,KV paramlist,out string result);       	
		
		//通用接口
		int RequestMisApi(Identity id,string method,KV paramlist,out string result);     
    };
    
    interface GoodsTrade
    {
		int TradeAPI(Identity id,string method,string params,out string result);
		int GoodsAPI(Identity id,string method,string params,out string result);
		int HpsAPI(Identity id,string method,string params,out string result);
    };
    
};

#endif

