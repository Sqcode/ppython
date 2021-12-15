package cn.su1888.cun.cb.constants;

/**
 * 
 * @description:电影票访问接口路径
 * @author: wangzuo chun
 * @version:  v0.1 
 * @time: 2018年5月27日 下午6:21:36
 */
public class MaoyanMovieURL {
	
	public static final String ULR_PREFIX = "http://api.filmfly.cn";
	
	public static final String MAOYAN_URL = "http://api.maoyan.com"; // 猫眼
	
	/**城市列表查询url*/
	public static final String MOVIE_CITY_LIST_URL = ULR_PREFIX + "/partner/ticketing/citylist";
	
	/**影院列表查询url*/
	public static final String MOVIE_CINEMA_LIST_URL = ULR_PREFIX + "/partner/ticketing/cinemalist";
	
	/**影院详情查询url*/
	public static final String MOVIE_CINEMA_INFO_URL = ULR_PREFIX + "/partner/ticketing/cinemainfo";
	
	/**影院影讯排期查询url*/
	public static final String MOVIE_PLAN_LIST_URL = ULR_PREFIX + "/partner/ticketing/planlist";
	
	/**获取场次座位图url*/
	public static final String MOVIE_SEAT_LIST_URL = ULR_PREFIX + "/partner/ticketing/seatlist";
	
	/**锁座接口url*/
	public static final String MOVIE_ORDER_CREATE_URL = ULR_PREFIX + "/partner/ticketing/ordercreate";	
	
	/**出票接口url*/
	public static final String MOVIE_ORDER_PAY_URL = ULR_PREFIX + "/partner/ticketing/orderpay";
	
	/**订单详情接口url*/
	public static final String MOVIE_ORDER_INFO_URL = ULR_PREFIX + "/partner/ticketing/orderinfo";
	
	/**解锁接口url*/
	public static final String MOVIE_ORDER_CANCEL_URL = ULR_PREFIX + "/partner/ticketing/ordercancel";
	
//	/** 猫眼 - 手机版影片搜索*/
//	public static final String MAOYAN_FILM_URL = "http://m.maoyan.com/ajax/search";
	
	/** 猫眼 - 影片详情 */
	public static final String MAOYAN_API_FILM_INFO_URL = MAOYAN_URL + "/mmdb/movie/v5/FILMID.json";
	
	/** 猫眼 - 影片、关联的演员 */
	public static final String MAOYAN_API_CELEBRITIES_URL = MAOYAN_URL + "/mmdb/movie/FILMID/role/celebrities.json";
	
	/** 猫眼 - 演员详情 */
	public static final String MAOYAN_API_CELEBRITY_INFO_URL = MAOYAN_URL + "/mmdb/v6/celebrity/CELEBRITYID.json";
	
	/** 猫眼 - 影片名称搜索，可拿到id等*/
	public static final String MAOYAN_API_FILM_URL = MAOYAN_URL + "/mmdb/search/integrated/keyword/list.json";
	
	https://maoyan.com/ajax/suggest?kw=%E6%98%8E%E6%97%A5%E4%B9%8B%E6%88%98
	
	/** 猫眼 - 影片剧照  FILMID：影片id*/
	public static final String MAOYAN_API_IMAGES_RESOURCES_URL = MAOYAN_URL + "/mmdb/movie/photos/FILMID/list.json";
	
	/** 猫眼 - 影片视频 */
	public static final String MAOYAN_API_FILM_VIDEOS_URL = MAOYAN_URL + "/mmdb/v1/movie/FILMID/videos.json";
	
	http://api.maoyan.com
	http://m.maoyan.com/mmdb/comments/movie/341516.json?_v_=yes&offset=2
	
}


1 1
2 1*15+1
3 2*15+1
4 3*15+1
5 4*15+1