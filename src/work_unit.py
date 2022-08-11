from typing import Tuple, List
import pymysql
import getpass
from env_logger import EnvLogger


class Job:
    def __init__(
        self,
        owner_id: int = 0,
        type: str = "",
        eb_url: str = "",
        cur_floor: str = "",
        mention_target: str = "",
    ) -> None:

        self.owner_id = owner_id
        self.type = type
        self.eb_url = eb_url
        self.cur_floor = cur_floor
        self.mention_target = mention_target

    # __init__()


# class Job


class Jobs:
    def __init__(self) -> None:
        self.__joblist = []

    # __init__()

    def new_job(
        self, owner_id: int, type: str, eb_url: str, cur_floor: str, mention_target: str
    ) -> Job:
        """Create new job object"""
        return Job(owner_id, type, eb_url, cur_floor, mention_target)

    # new_job()

    def get_jobs(self) -> List[Job]:
        """
        Get job list.
        return List[Job]
        """
        return self.__joblist

    # get_jobs()

    def same_job_existed(self, eb_url: str) -> int:
        """
        Check if there is already a job in the job list that has the same url as the new job.\n
        If yes, return job' s owner id or id will be -1.\n
        return owner id
        """

        if len(self.__joblist) == 0:
            return -1

        for job in self.__joblist:
            if job.eb_url == eb_url:
                return job.owner_id
            # if
        # for

        return -1

    # same_job_existed()

    def load_jobs(self, jobs: List[Job]) -> None:
        """Load jobs from given job list"""
        self.__joblist = jobs

    # load_jobs()

    def add_job(self, job: Job) -> None:
        """Add job to job list, if there is no collision."""
        self.__joblist.append(job)

    # add_job()

    def delete_job(self, eb_url: str) -> None:
        """Delete job from job list, if there is a job matched."""

        for job in self.__joblist:
            if job.eb_url == eb_url:
                self.__joblist.remove(job)
            # if
        # for

    # delete_job()

    def update_job(self, eb_url: str, new_price: str) -> None:
        """Update job floor price in job list, if there is a job matched."""
        for job in self.__joblist:
            if job.eb_url == eb_url:
                job.cur_floor = new_price
            # if
        # for

    # update_job()


# class Jobs


class MintTracker:
    def __init__(
        self,
        contract_addr: str = "",
        token_name: str = "",
        total_supply: str = "",
        cur_supply: str = "0",
    ) -> None:
        self.contract_addr = contract_addr
        self.token_name = token_name
        self.total_supply = total_supply
        self.cur_supply = cur_supply

    # __init__()


# class MintTracker


class MintTrackers:
    def __init__(self) -> None:
        self.__mint_trackers = []

    # __init__()

    def new_tracker(
        self,
        contract_addr: str = "",
        token_name: str = "",
        total_supply: str = "",
        cur_supply: str = "0",
    ) -> MintTracker:
        """Create new mint tracker object"""
        return MintTracker(contract_addr, token_name, total_supply, cur_supply)

    # new_mint_tracker()

    def same_tracker_existed(self, contract_addr: str) -> bool:
        for tracker in self.__mint_trackers:
            if tracker.contract_addr == contract_addr:
                return True
        # for

        return False

    # same_tracker_existed()

    def load_mint_trackers(self, trackers: List[MintTracker]) -> None:
        """Load jobs from given job list"""
        self.__mint_trackers = trackers

    # load_mint_trackers()

    def get_trackers(self) -> List[MintTracker]:
        """
        Get all tracker in tracker list.
        return List[MintTracker]
        """
        return self.__mint_trackers

    # get_trackers()

    def add_tracker(self, tracker: MintTracker) -> None:
        """Add tracker to mint tracker list, if there is no collision."""
        self.__mint_trackers.append(tracker)

    # add_tracker()

    def delete_tracker(self, contract_addr: str) -> None:
        """Delete tracker from mint tracker list, if there is existed."""
        for tracker in self.__mint_trackers:
            if tracker.contract_addr == contract_addr:
                self.__mint_trackers.remove(tracker)
            # if
        # for

    # delete_tracker()

    def update_tracker(self, contract_addr: str, new_cur_supply: str) -> None:
        """Update tracker current supply in mint tracker list."""
        for tracker in self.__mint_trackers:
            if tracker.contract_addr == contract_addr:
                tracker.cur_supply = new_cur_supply
            # if
        # for

    # update_tracker()


# class MintTrackers


class SqlDB:
    def __init__(self):
        self.__db = None  # connection pointer
        self.__logger = EnvLogger("SqlDB.cls")

    # __init__()

    def connect(self) -> Tuple[bool, str]:
        """
        Connect local sql db.\n
        If fail, success will be False with a reason.\n
        return ( success, reason )
        """
        passwd = getpass.getpass("DB password:")

        try:
            self.__db = pymysql.connect(
                host="localhost",
                port=3306,
                user="root",
                passwd=passwd,
                db="ebisu_tracker",
                charset="utf8",
            )
            return (True, "")
        # try

        except Exception as e:
            self.__logger.critical(e)
            return (False, "資料庫連線失敗")
        # except

    # connect()

    def disconnect(self) -> str:
        """
        Disconnect db server.\n
        return success
        """
        self.__db.close()

        return "已中斷資料庫連線"

    # disconnect()

    def insert_job(self, job: Job) -> Tuple[bool, str]:
        """
        Insert a job record to db.\n
        If fail, success will be False with a reason.\n
        return ( success, reason )
        """
        cursor = self.__db.cursor()

        sql = (
            "INSERT INTO jobs ( OWNER_ID, TYPE, EB_URL, CUR_FLOOR, MENTION_TARGET ) VALUES "
            + f"( {job.owner_id}, '{job.type}', '{job.eb_url}', '{job.cur_floor}', '{job.mention_target}' )"
        )

        try:
            cursor.execute(sql)
            self.__db.commit()
            return (True, "")
        # try

        except Exception as e:
            self.__logger.error(e)
            self.__db.rollback()
            return (False, "資料庫發生寫入錯誤")
        # except

    # insert_job()

    def delete_specific_job(self, url: str) -> Tuple[bool, str]:
        """
        Delete a job record in db.\n
        If fail, success will be False with a reason.\n
        return ( success, reason )
        """
        cursor = self.__db.cursor()

        sql = f"DELETE FROM jobs WHERE EB_URL = '{url}'"

        try:
            cursor.execute(sql)
            self.__db.commit()
            return (True, "")
        # try

        except Exception as e:
            self.__logger.error(e)
            self.__db.rollback()
            return (False, "資料庫發生刪除錯誤")
        # except

    # delete_specific_job()

    def update_specific_job_floor(self, url: str, new_floor: str) -> Tuple[bool, str]:
        """
        Update a job floor price record in db.\n
        If fail, success will be False with a reason.\n
        return ( success, reason )
        """
        cursor = self.__db.cursor()

        sql = f"UPDATE jobs SET CUR_FLOOR = '{new_floor}' WHERE EB_URL = '{url}'"

        try:
            cursor.execute(sql)
            self.__db.commit()
            return (True, "")
        # try

        except Exception as e:
            self.__logger.error(e)
            self.__db.rollback()
            return (False, "資料庫發生更新錯誤")
        # except

    # update_specific_job()

    def fetch_all_jobs(self) -> Tuple[bool, str, List[Job]]:
        """
        Fetch all job records from db.\n
        If fail, success will be False with a reason.\n
        return ( success, reason, [Jobs] )
        """
        cursor = self.__db.cursor()

        sql = "SELECT * FROM jobs"

        try:
            cursor.execute(sql)
            db_jobs = list(cursor.fetchall())
            jobs = []

            for db_job in db_jobs:
                job = Job()
                job.owner_id = db_job[0]
                job.type = db_job[1]
                job.eb_url = db_job[2]
                job.cur_floor = db_job[3]
                job.mention_target = db_job[4]

                jobs.append(job)
            # for

            return (True, "", jobs)
        # try

        except Exception as e:
            self.__logger.error(e)
            return (False, "資料庫發生讀取錯誤", [])
        # except

    # fetch_all_jobs()

    def insert_mint_tracker(self, tracker: MintTracker) -> Tuple[bool, str]:
        """
        Insert a mint tracker record to db.\n
        If fail, success will be False with a reason.\n
        return ( success, reason )
        """
        cursor = self.__db.cursor()

        sql = (
            "INSERT INTO mint_trackers ( TOKEN_NAME, CONTRACT_ADDR, TOTAL_SUPPLY, CUR_SUPPLY ) "
            + f"VALUES ( '{tracker.token_name}', '{tracker.contract_addr}', '{tracker.total_supply}', "
            + f"'{tracker.cur_supply}' )"
        )

        try:
            cursor.execute(sql)
            self.__db.commit()
            return (True, "")
        # try

        except Exception as e:
            self.__logger.error(e)
            self.__db.rollback()
            return (False, "資料庫發生寫入錯誤")
        # except

    # insert_mint_tracker()

    def delete_specific_mint_tracker(self, contract_addr: str) -> Tuple[bool, str]:
        """
        Delete a mint tracker record in db.\n
        If fail, success will be False with a reason.\n
        return ( success, reason )
        """
        cursor = self.__db.cursor()

        sql = f"DELETE FROM mint_trackers WHERE CONTRACT_ADDR = '{contract_addr}'"

        try:
            cursor.execute(sql)
            self.__db.commit()
            return (True, "")
        # try

        except Exception as e:
            self.__logger.error(e)
            self.__db.rollback()
            return (False, "資料庫發生刪除錯誤")
        # except

    # delete_specific_trackers()

    def update_specific_mint_tracker(
        self, contract_addr: str, new_cur_supply: str
    ) -> Tuple[bool, str]:
        """
        Update a mint tracker cur_supply record in db.\n
        If fail, success will be False with a reason.\n
        return ( success, reason )
        """
        cursor = self.__db.cursor()

        sql = (
            f"UPDATE mint_trackers SET CUR_SUPPLY = '{new_cur_supply}' "
            + f"WHERE CONTRACT_ADDR = '{contract_addr}'"
        )

        try:
            cursor.execute(sql)
            self.__db.commit()
            return (True, "")
        # try

        except Exception as e:
            self.__logger.error(e)
            self.__db.rollback()
            return (False, "資料庫發生更新錯誤")
        # except

    # update_specific_mint_tracker()

    def fetch_all_mint_trackers(self) -> Tuple[bool, str, List[MintTracker]]:
        """
        Fetch all mint tracker records from db.\n
        If fail, success will be False with a reason.\n
        return ( success, reason, [MintTracker] )
        """
        cursor = self.__db.cursor()

        sql = "SELECT * FROM mint_trackers"

        try:
            cursor.execute(sql)
            db_mint_trackers = list(cursor.fetchall())
            mint_trackers = []

            for db_job in db_mint_trackers:
                tracker = MintTracker()
                tracker.token_name = db_job[0]
                tracker.contract_addr = db_job[1]
                tracker.total_supply = db_job[2]
                tracker.cur_supply = db_job[3]

                mint_trackers.append(tracker)
            # for

            return (True, "", mint_trackers)
        # try

        except Exception as e:
            self.__logger.error(e)
            return (False, "資料庫發生讀取錯誤", [])
        # except

    # fetch_all_mint_trackers()

    def fetch_ramdom_record_east(self) -> Tuple[bool, str, dict]:
        """
        Fetch random record from fishing east table.\n
        If fail, success will be False with a reason.\n
        return ( success, reason, dict )
        """
        cursor = self.__db.cursor()

        sql = (
            "SELECT * FROM `fishing_e` WHERE id >= ((SELECT MAX(id) FROM fishing_e)"
            + "- (SELECT MIN(id) FROM fishing_e)) * RAND() + (SELECT MIN(id) FROM fishing_e) LIMIT 1"
        )

        try:
            cursor.execute(sql)
            record = cursor.fetchall()[0]
            result = {
                "ID": f"E.{record[0]}",
                "NAME": record[1],
                "LUCKY": record[2],
                "DESCRIPTION": record[3],
            }
            return (True, "", result)
        # try

        except Exception as e:
            self.__logger.error(e)
            return (False, "資料庫發生讀取錯誤", {})
        # except

    # fetch_ramdom_record_east()

    def fetch_ramdom_record_west(self) -> Tuple[bool, str, dict]:
        """
        Fetch random record from fishing west table.\n
        If fail, success will be False with a reason.\n
        return ( success, reason, dict )
        """
        cursor = self.__db.cursor()

        sql = (
            "SELECT * FROM `fishing_w` WHERE id >= ((SELECT MAX(id) FROM fishing_w)"
            + "- (SELECT MIN(id) FROM fishing_w)) * RAND() + (SELECT MIN(id) FROM fishing_w) LIMIT 1"
        )

        try:
            cursor.execute(sql)
            record = cursor.fetchall()[0]
            result = {
                "ID": f"W.{record[0]}",
                "NAME": record[1],
                "LUCKY": record[2],
                "DESCRIPTION": record[3],
            }
            return (True, "", result)
        # try

        except Exception as e:
            self.__logger.error(e)
            return (False, "資料庫發生讀取錯誤", {})
        # except

    # fetch_ramdom_record_west()

    def fetch_ramdom_record_south(self) -> Tuple[bool, str, dict]:
        """
        Fetch random record from fishing south table.\n
        If fail, success will be False with a reason.\n
        return ( success, reason, dict )
        """
        cursor = self.__db.cursor()

        sql = (
            "SELECT * FROM `fishing_s` WHERE id >= ((SELECT MAX(id) FROM fishing_s)"
            + "- (SELECT MIN(id) FROM fishing_s)) * RAND() + (SELECT MIN(id) FROM fishing_s) LIMIT 1"
        )

        try:
            cursor.execute(sql)
            record = cursor.fetchall()[0]
            result = {
                "ID": f"S.{record[0]}",
                "NAME": record[1],
                "LUCKY": record[2],
                "DESCRIPTION": record[3],
            }
            return (True, "", result)
        # try

        except Exception as e:
            self.__logger.error(e)
            return (False, "資料庫發生讀取錯誤", {})
        # except

    # fetch_ramdom_record_south()

    def fetch_ramdom_record_north(self) -> Tuple[bool, str, dict]:
        """
        Fetch random record from fishing north table.\n
        If fail, success will be False with a reason.\n
        return ( success, reason, dict )
        """
        cursor = self.__db.cursor()

        sql = (
            "SELECT * FROM `fishing_n` WHERE id >= ((SELECT MAX(id) FROM fishing_n)"
            + "- (SELECT MIN(id) FROM fishing_n)) * RAND() + (SELECT MIN(id) FROM fishing_n) LIMIT 1"
        )

        try:
            cursor.execute(sql)
            record = cursor.fetchall()[0]
            result = {
                "ID": f"N.{record[0]}",
                "NAME": record[1],
                "LUCKY": record[2],
                "DESCRIPTION": record[3],
            }
            return (True, "", result)
        # try

        except Exception as e:
            self.__logger.error(e)
            return (False, "資料庫發生讀取錯誤", {})
        # except

    # fetch_ramdom_record_north()


# class SqlDB


class Scheduler:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    # __new__()

    def __init__(self) -> None:
        self.__db = SqlDB()
        self.__job_controller = Jobs()
        self.__mint_controller = MintTrackers()
        self.__logger = EnvLogger("Scheduler.cls")

    # __init__()

    def start(self) -> Tuple[bool, str]:
        """
        Connect db.\n
        If fail, success will be False with a reason.\n
        return ( success, reason )
        """
        return self.__db.connect()

    # start()

    def rest(self):
        """disconnect db"""
        return self.__db.disconnect()

    # rest()

    def load_jobs(self) -> Tuple[bool, str]:
        """Load jobs from job given list"""
        (success, reason, job_list) = self.__db.fetch_all_jobs()

        if success:
            self.__job_controller.load_jobs(job_list)
            return (True, "")
        # if

        return (False, reason)

    # load_jobs()

    def get_jobs(self) -> List[Job]:
        """
        Get all jobs in job list.
        return List[Job]
        """
        return self.__job_controller.get_jobs()

    # get_jobs()

    def add_job(
        self,
        ctx_author_id: int,
        type: str,
        eb_url: str,
        floor_price: str,
        mention_target: str,
    ) -> Tuple[bool, str]:
        """
        Add job to job list, if there is no collision.\n
        return ( success, reason )
        """
        owner_id = self.__job_controller.same_job_existed(eb_url)

        if owner_id != -1:
            reason = (
                f"已存在相同追蹤目標，請聯繫任務擁有者 <@{owner_id}> "
                + "考慮是否需要合併任務，如您即為擁有者，想變更設定，請使用 `/delete [url]` 先刪除任務"
            )
            return (False, reason)
        # if

        job = self.__job_controller.new_job(
            ctx_author_id, type, eb_url, floor_price, mention_target
        )
        (success, reason) = self.__db.insert_job(job)

        if not success:
            return (False, reason)

        self.__job_controller.add_job(job)
        return (True, "")

    # add_job()

    def delete_job(self, ctx_author_id: int, eb_url: str) -> Tuple[bool, str]:
        """
        Delete job from job list, if there is a job matched.\n
        return ( success, reason )
        """

        owner_id = self.__job_controller.same_job_existed(eb_url)

        if owner_id == -1:
            return (False, "不存在的任務")

        elif ctx_author_id != owner_id:
            return (False, f"您非任務持有者，請聯繫任務擁有者 <@{owner_id}> 考慮是否需要做任務變更")

        else:
            (success, reason) = self.__db.delete_specific_job(eb_url)

            if success:
                self.__job_controller.delete_job(eb_url)
                return (True, "")
            # if
            else:
                return (False, reason)
        # else

    # delete_job()

    def update_job(self, eb_url: str, new_price: str) -> Tuple[bool, str]:
        """
        For Update job floor price in job list, if there is a job matched.\n
        return ( success, reason )
        """

        owner_id = self.__job_controller.same_job_existed(eb_url)

        if owner_id == -1:
            return (False, "不存在的任務")

        else:
            (success, reason) = self.__db.update_specific_job_floor(eb_url, new_price)

            if success:
                self.__job_controller.update_job(eb_url, new_price)
                return (True, "")
            # if
            else:
                return (False, reason)
        # else

    # update_job()

    def get_mint_trackers(self) -> List[MintTracker]:
        """
        Get all tracker in tracker list.
        return List[MintTracker]
        """
        return self.__mint_controller.get_trackers()

    # get_jobs()

    def load_mint_trackers(self) -> Tuple[bool, str]:
        """Load trackers from tracker given list"""
        (success, reason, tracker_list) = self.__db.fetch_all_mint_trackers()

        if success:
            self.__mint_controller.load_mint_trackers(tracker_list)
            return (True, "")
        # if

        return (False, reason)

    # load_mint_trackers()

    def add_mint_tracker(
        self, contract_addr: str, token_name: str, total_supply: str, cur_supply: str
    ) -> Tuple[bool, str]:
        """
        Add tracker to mint tracker list, if there is no collision.\n
        return ( success, reason )
        """

        if self.__mint_controller.same_tracker_existed(contract_addr):
            reason = "已存在相同追蹤目標"
            return (False, reason)
        # if

        tracker = self.__mint_controller.new_tracker(
            contract_addr, token_name, total_supply, cur_supply
        )
        (success, reason) = self.__db.insert_mint_tracker(tracker)

        if not success:
            return (False, reason)

        self.__mint_controller.add_tracker(tracker)
        return (True, "")

    # add_tracker()

    def delete_mint_tracker(self, contract_addr: str) -> Tuple[bool, str]:
        """
        Delete tracker from mint tracker list, if there is existed.\n
        return ( success, reason )
        """
        if not (self.__mint_controller.same_tracker_existed(contract_addr)):
            reason = "不存在的追蹤目標"
            return (False, reason)
        # if

        (success, reason) = self.__db.delete_specific_mint_tracker(contract_addr)

        if not success:
            return (False, reason)

        self.__mint_controller.delete_tracker(contract_addr)
        return (True, "")

    # delete_mint_tracker()

    def update_tracker(
        self, contract_addr: str, new_cur_supply: str
    ) -> Tuple[bool, str]:
        """
        Update tracker current supply in mint tracker list.\n
        return ( success, reason )
        """
        if not (self.__mint_controller.same_tracker_existed(contract_addr)):
            reason = "不存在的追蹤目標"
            return (False, reason)
        # if

        (success, reason) = self.__db.update_specific_mint_tracker(
            contract_addr, new_cur_supply
        )

        if not success:
            return (False, reason)

        self.__mint_controller.update_tracker(contract_addr, new_cur_supply)
        return (True, "")

    # update_tracker()

    def fetch_ramdom_record_from(self, position: str) -> Tuple[bool, dict]:
        """
        Fetch random record from a fishing table of position.\n
        Support: EAST, WEST, SOUTH, NORTH\n
        If fail, success will be False with a reason.\n
        return ( success, reason, dict )
        """
        if position == "EAST":
            (success, reason, result) = self.__db.fetch_ramdom_record_east()
        elif position == "WEST":
            (success, reason, result) = self.__db.fetch_ramdom_record_west()
        elif position == "SOUTH":
            (success, reason, result) = self.__db.fetch_ramdom_record_south()
        elif position == "NORTH":
            (success, reason, result) = self.__db.fetch_ramdom_record_north()
        else:
            self.__logger.warning("Not supported position.")
            return (False, {})
        # else

        if not success:
            self.__logger.warning(reason)
            return (False, {})
        # if

        return (True, result)

    # fetch_ramdom_record_from()


# class Scheduler
