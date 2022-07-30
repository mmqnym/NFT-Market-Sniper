import os
import discord
from discord import Option, OptionChoice 
from discord.ext import tasks, commands, pages
from discord.ext.pages import Page, Paginator
from datetime import datetime
import asyncio
from typing import *
import random

from configs import Configs
from work_unit import Scheduler
from tracker import Tracker
from dc_extend import *
from cmc_function import CMCFunction

from env_logger import EnvLogger

''' Control all global configs. '''
CFG = Configs()

''' Record all job and mint_tracker, also control DB. '''
SCHEDULER = Scheduler()

''' Track all url in todo list by tracker. '''
TRACKER = None

''' Caller for CoinMarketCap function. '''
CMCFUNC = None

''' Check bot is first excution. '''
first_exec = False

MAIN_LOGGER = EnvLogger( 'main.mod', 'info' )

bot = discord.Bot( intents = discord.Intents.all(),
                   owner_id = CFG.get_owner_id(),
                   activity = discord.Activity( type = discord.ActivityType.watching, name = 'Ebisu\'s bay' ),
                   status = discord.Status.online )


def main() -> None:
    ''' Start from here '''
    global CFG, SCHEDULER, TRACKER, CMCFUNC, MAIN_LOGGER

    ( success, reason ) = CFG.init()

    if ( success ):
        bot_token = CFG.get_bot_token()

        if ( bot_token == 'Your Token' or CFG.get_owner_id() == 0 or CFG.get_system_log_channel() == 0 or
             CFG.get_cronoscan_api_key() == 'Your Key' or CFG.get_cmc_api_key() == 'Your Key' ):
            MAIN_LOGGER.critical( '請先在 src/configs.json 中寫入' + 
                                  'BOT_TOKEN, OWNER_ID, TARGET_CHANNEL_FOR_SYSTEM_LOG, CRONOSCAN_API_KEY, ' + 
                                  'COINMARKETCAP_API_KEY 的值' )
            return
        # if

        TRACKER = Tracker( CFG.get_cronoscan_api_key() )
        CMCFUNC = CMCFunction( CFG.get_cmc_api_key() )

        MAIN_LOGGER.info( '開始連線資料庫...' )
        ( success, reason ) = SCHEDULER.start()

        if not success:
            MAIN_LOGGER.critical( reason )
            return
        # while

        MAIN_LOGGER.info( '資料庫已連線' )

        ( success, reason ) = SCHEDULER.load_jobs()

        if not success:
            MAIN_LOGGER.critical( '無法從資料庫載入 job 清單' )
            return
        # if

        ( success, reason ) = SCHEDULER.load_mint_trackers()

        if not success:
            MAIN_LOGGER.critical( '無法從資料庫載入 mint tracker 清單' )
            return
        # if
    
        MAIN_LOGGER.info( '機器人相關預備程序已完成.. 等待連結伺服器' )
        
        bot.run( bot_token )

        ''' Deprecated
        (※Somehow this causes serious delays in this bot. 
        This seems to stem from the lack of functionality of asyncio on windows.)
        
        asyncio.set_event_loop_policy( asyncio.WindowsSelectorEventLoopPolicy() )

        try:
            asyncio.run( bot.start( bot_token ) )
        except KeyboardInterrupt:
            asyncio.run( bot.close() )
        '''
    # if

    else:
        MAIN_LOGGER.critical( f'機器人初始化失敗，請重新啟動: {reason}' )
# main()

def make_embed( title:str = None, description:str = None, color:discord.Colour = None, 
                is_local_image:bool = False, image_url:str = None, file:'discord.File' = None,
                thumbnail_url:str = None, more_fields:Optional[List[list]] = None ) -> 'discord.Embed':
    ''' 
    A simply way to make a embed with some settings.\n
    return discord.Embed
    '''

    if ( is_local_image and 'attachment://' not in image_url ) and file is None:
        raise Exception( 'Local image flag is Set, but not match format or file is not submitted.' )

    t_title = ''
    t_description = ''

    if not ( title is None ):
        t_title = title

    if not ( description is None ):
        t_description = description

    t_embed = discord.Embed( title = t_title, description = t_description, color = color )
    t_embed.set_author( name = 'EB Extend BOT',
                        url = 'https://twitter.com/0xmimiQ',
                        icon_url = 'https://i.imgur.com/DmV9HWw.png' )
    
    if not ( thumbnail_url is None or thumbnail_url == '' ):
        t_embed.set_thumbnail( url = thumbnail_url )

    if not ( more_fields is None ):
        for field in more_fields:
            t_embed.add_field( name = field[0], value = field[1], inline = field[2] )
    # if

    if not ( image_url is None ):
        t_embed.set_image( url = image_url )

    t_embed.timestamp = datetime.now()
    t_embed.set_footer( text = 'Ebisu\'s Extend Bot' )

    return t_embed
# make_embed()

def dc_color( color_name:str ) -> discord.Colour:
    ''' return discord rgb color '''
    if color_name == 'red':
        return discord.Colour.from_rgb( 227, 4, 4 )
    elif color_name == 'purple':
        return discord.Colour.from_rgb( 222, 199, 241 )
    elif color_name == 'green':
        return discord.Colour.from_rgb( 16, 172, 3 )
    elif color_name == 'l_blue':
        return discord.Colour.from_rgb( 0, 255, 255 ) 
    else:
        return discord.Colour.from_rgb( 255, 255, 255 )
# dc_color()

def task_loop( mode:str ) -> None:
    ''' Get discord tasks event loop to do 'start' or 'stop'. '''
    global MAIN_LOGGER

    if mode.lower() == 'start':
        if track_mint_status.is_running() or track_floor_price.is_running():
            return

        MAIN_LOGGER.info( '開始任務循環' )
        track_mint_status.start()
        track_floor_price.start()
    # if
    
    elif mode.lower() == 'stop':
        MAIN_LOGGER.info( '結束任務循環' )
        track_mint_status.stop()
        track_floor_price.stop()
    # elif
    
    else:
        raise Exception( 'Not supported mode. support: \'start\', \'stop\'' )
# exec_task

@bot.event
async def on_ready() -> None:
    global CFG, SCHEDULER, first_exec, MAIN_LOGGER, TRACKER

    MAIN_LOGGER.info( f'已連結官方伺服器.. 目前登入身份：{bot.user}' )
    channel = ''

    try:
        channel = await bot.fetch_channel( CFG.get_system_log_channel() )

        if not first_exec:
            embed = make_embed( description = '機器人已成功連結伺服器', color = dc_color( 'green' ),
                                thumbnail_url = CFG.get_hello_and_bye_img_url() )
            await channel.send( embed = embed )
            first_exec = True
        # if
    # try
    except Exception as e:
        MAIN_LOGGER.critical( e )
        bot.loop.run_until_complete( bot.close() )
        return
    # except

    if not TRACKER.browser_is_running:
        await TRACKER.launch_browser()
    task_loop( 'start' )

# on_ready()


''' Discord Commands Below'''

''' Command groups '''
sys = bot.create_group( name = 'sys', description = 'System command.' )
set = bot.create_group( name = 'set', description = 'Set tracker.' )
delete = bot.create_group( name = 'delete', description = 'Delete tracker.' )
list = bot.create_group( name = 'list', description = 'List tracker(s).' )
convert = bot.create_group( name = 'convert', description = 'Convert currencies.' )

track_type = [
    OptionChoice( name = 'system', value = 'system' ),
    OptionChoice( name = 'floor', value = 'floor' ),
    OptionChoice( name = 'mint', value = 'mint' )
]

@bot.slash_command( name = 'bind', description = 'Bind a channel to send system / mint status / floor price info.' )
@commands.is_owner()
@commands.cooldown( 1, 15, commands.BucketType.user )
async def bind( ctx:discord.ApplicationContext, 
                type:Option( str, 'Choose tracker type.', choices = track_type ), 
                channel:Option( discord.TextChannel, 'Choose a channel' ) ) -> None:
    ''' Bind a channel to send system / mint status / floor price info. '''
    global CFG

    type = type.lower()

    success = False
    reason = ''

    if type == 'system':
        ( success, reason ) = CFG.set_system_log_channel( channel.id )
    elif type == 'floor':
        ( success, reason ) = CFG.set_floor_tracker_channel( channel.id )
    else:
        ( success, reason ) = CFG.set_mint_tracker_channel( channel.id )

    if not success:
        embed = make_embed( description = reason, color = dc_color( 'red' ), thumbnail_url = CFG.get_error_img_url() )
    else:
        embed = make_embed( description = f'推送頻道 [{type}] 已綁定: {channel.mention}',
                            color = dc_color( 'green' ), thumbnail_url = CFG.get_done_img_url() )

    await ctx.respond( embed = embed )
# bind()

page_buttons = [
    pages.PaginatorButton( 'first', emoji = '⏪', style = discord.ButtonStyle.gray ),
    pages.PaginatorButton( 'prev', emoji = '◀', style = discord.ButtonStyle.gray ),
    pages.PaginatorButton( 'page_indicator', style = discord.ButtonStyle.gray, disabled = True ),
    pages.PaginatorButton( 'next', emoji = "▶", style = discord.ButtonStyle.gray ),
    pages.PaginatorButton( 'last', emoji = "⏩", style = discord.ButtonStyle.gray )
]

@list.command( name = 'all_jobs', description = 'List all floor tracker jobs.' )
@commands.cooldown( 1, 15, commands.BucketType.user )
async def list_all_jobs( ctx:discord.ApplicationContext ) -> None:
    ''' List all floor trackers '''
    global SCHEDULER

    job_pages = []
    page_num = 0

    t_embed = discord.Embed( title = '', description = '當前所有任務清單', color = dc_color('purple') )
    jobs = SCHEDULER.get_jobs()

    if len( jobs ) == 0:
        await ctx.respond( embed = t_embed )
        return
    # if

    i = 0

    for job in jobs:
        i += 1

        series = ( job.eb_url ).replace( 'https://app.ebisusbay.com/collection/', '' )
        t_embed.add_field( name = '任務擁有者', value = f'<@{job.owner_id}>', inline = False )
        t_embed.add_field( name = '目標系列', value = f'[{series}]({job.eb_url})', inline = True )
        t_embed.add_field( name = '當前地板價', value = f'`{job.cur_floor} CRO`', inline = True )
        t_embed.add_field( name = '通知對象', value = job.mention_target, inline = True )
    
        if i % 3 == 0:
            page_num = i // 3
            new_page = Page( content = f'Page {page_num} / ', embeds = [t_embed] )
            job_pages.append( new_page )
            t_embed = discord.Embed( title = '', description = '當前所有任務清單', color = dc_color('purple') )
        # if
    # for

    if i % 3 > 0:
        page_num += 1
        new_page = Page( content = f'Page {page_num} / ', embeds = [t_embed] )
        job_pages.append( new_page )
    # if
    
    total_jobs = len( job_pages )

    for page in job_pages:
        page.content += str( total_jobs )

    paginator = Paginator( pages = job_pages, loop_pages = True, disable_on_timeout = True, show_indicator = False,
                           use_default_buttons = False, custom_buttons = page_buttons, timeout = 60 )
    await paginator.respond( ctx.interaction, ephemeral = False )
    
# list_all_jobs()

@list.command( name = 'jobs', description = 'List a person\'s floor tracker jobs.' )
@commands.cooldown( 1, 15, commands.BucketType.user )
async def list_jobs( ctx:discord.ApplicationContext, user:Option( discord.User, 'Tag a person.') ) -> None:
    ''' List a specific person's floor trackers. '''
    global SCHEDULER

    job_pages = []
    page_num = 0

    source_id = user.id

    t_embed = discord.Embed( title = '', description = f'{user.mention} 的任務清單', color = dc_color( 'purple' ) )
    jobs = SCHEDULER.get_jobs()

    if len( jobs ) == 0:
        t_embed.description += ': 查無任何任務'
        await ctx.respond( embed = t_embed )
        return
    # if

    i = 0

    for job in jobs:
        if source_id == job.owner_id:
            i += 1

            series = ( job.eb_url ).replace( 'https://app.ebisusbay.com/collection/', '' )
            t_embed.add_field( name = '目標系列', value = f'[{series}]({job.eb_url})', inline = True )
            t_embed.add_field( name = '當前地板價', value = f'`{job.cur_floor} CRO`', inline = True )
            t_embed.add_field( name = '通知對象', value = job.mention_target, inline = True )
        
            if i % 3 == 0:
                page_num = i // 3
                new_page = Page( content = f'Page {page_num} / ', embeds = [t_embed] )
                job_pages.append( new_page )
                t_embed = discord.Embed( title = '',  description = '當前所有任務清單', color = dc_color('purple') )
            # if
        # if
    # for

    if i == 0:
        t_embed.description += ': 查無任何任務'
        await ctx.respond( embed = t_embed )
        return
    # if

    if i % 3 > 0:
        page_num += 1
        new_page = Page( content = f'Page {page_num} / ', embeds = [t_embed] )
        job_pages.append( new_page )
    # if

    for page in job_pages:
        page.content += str( len( job_pages ) )

    paginator = Paginator( pages = job_pages, loop_pages = True, disable_on_timeout = True, show_indicator = False,
                           use_default_buttons = False, custom_buttons = page_buttons, timeout = 60 )
    await paginator.respond( ctx.interaction, ephemeral = False )

# list_jobs()

@set.command( name = 'floor_tracker',
              description = 'Set a Tracker to track the floor price of collection by Ebisu\'s bay collection url.' )
@commands.cooldown( 1, 15, commands.BucketType.user )
async def set_floor_tracker( ctx:discord.ApplicationContext,
                             url:Option( str, 'Enter a Ebisu\'s bay collection url.' ) ) -> None:
    ''' Set a tracker to track the floor price of collection by Ebisu\' s bay collection url. '''
    global SCHEDULER, TRACKER, CFG

    if CFG.get_floor_tracker_channel() == 0:
        embed = make_embed( description = f'您必須先設定地板價變動發送頻道 參考：`/bind`', color = dc_color( 'red' ),
                            thumbnail_url = CFG.get_error_img_url())
        await ctx.respond( embed = embed )
        return
    # if
    
    if 'https://app.ebisusbay.com/collection/' not in url:
        msg = '無效的網址參數，請輸入 ebisu collection 網址, use case: `/track https://app.ebisusbay.com/collection/xxx`'

        embed = make_embed( description = msg, color = dc_color( 'red' ), thumbnail_url = CFG.get_error_img_url() )
        await ctx.respond( embed = embed )
    # if

    else:
        embed = make_embed( description = '檢驗是否為存在的 Ebisu\'s bay 收藏，請稍後...', color = dc_color('purple') )
        sent_msg = await ctx.respond( embed = embed )
        
        ( erc_type, floor_price ) = await TRACKER.track_floor( url )

        if ( floor_price == '' ):
            msg = '不存在的 Ebisu collection 或 Ebisu API 故障: [狀態檢查](https://status.ebisusbay.com/)'

            embed = make_embed( description = msg, color = dc_color('red'), thumbnail_url = CFG.get_error_img_url() )
            await sent_msg.edit_original_message( embed = embed )
        # if

        else:
            embed = make_embed( description = ctx.author.mention + ' 請TAG您想通知的身分組或個人',
                                color = dc_color('purple') )
            await sent_msg.edit_original_message( embed = embed )

            usr_answer = await bot.wait_for( 'message', check = lambda msg: msg.author == ctx.author )
            mention_target = usr_answer.content
            await usr_answer.delete()
            series = url.replace( 'https://app.ebisusbay.com/collection/', '' )

            if ( '<@&' == mention_target[0:3] and '>' == mention_target[-1] ) or \
               ( '<@' == mention_target[0:2] and '>' == mention_target[-1] ):
                
                ( success, reason ) = SCHEDULER.add_job( ctx.author.id, erc_type, url, floor_price, mention_target )

                if not success:
                    embed = make_embed( description = reason, color = dc_color( 'red' ),
                                        thumbnail_url = CFG.get_error_img_url() )
                    await sent_msg.edit_original_message( embed = embed )
                # if

                else:
                    t_list = [ ['任務擁有者', ctx.author.mention, False],
                               ['目標系列', f'[{series}]({url})', True],
                               ['當前地板價', f'`{floor_price} CRO`', True],
                               ['通知對象', mention_target, True]
                             ]
                                  
                    embed = make_embed( title = '已成功設定追蹤', description = f'類型: ERC{erc_type}',
                                        color = dc_color( 'green' ), thumbnail_url = CFG.get_done_img_url(),
                                        more_fields = t_list )
                    await sent_msg.edit_original_message( embed = embed )
                # else

            # if
            else:
                embed = make_embed( description = '錯誤的tag參數，請確認您tag的是否為身份組或個人',
                                    color = dc_color( 'red' ), thumbnail_url = CFG.get_error_img_url() )
                await sent_msg.edit_original_message( embed = embed )
            # else
        # else
    # else

# set_floor_tracker()

@delete.command( name = 'floor_tracker', description = 'Delete an existing job.' )
@commands.cooldown( 1, 15, commands.BucketType.user )
async def delete_floor_tracker( ctx:discord.ApplicationContext, 
                                url:Option( str, 'Enter a Ebisu\'s bay collection url which in the record.' ) ) -> None:
    ''' Delete an existing job from the job list. '''
    global SCHEDULER, TRACKER
    
    ( success, reason ) = SCHEDULER.delete_job( ctx.author.id, url )

    if not success:
        embed = make_embed( description = reason, color = dc_color( 'red' ), thumbnail_url = CFG.get_error_img_url() )
        await ctx.respond( embed = embed )
    # if

    else:
        series = url.replace( 'https://app.ebisusbay.com/collection/', '' )
        description = f'您的任務已刪除： [{series}]({url})'
        embed = make_embed( description = description, color = dc_color( 'green' ),
                            thumbnail_url = CFG.get_done_img_url() )
        await ctx.respond( embed = embed )
    # else
# delete_floor_tracker()

@set.command( name = 'mint_tracker', 
              description = 'Set a tracker to watch one\'s collection mint status. (current total supply)' )
@commands.is_owner()
@commands.cooldown( 1, 15, commands.BucketType.user )
async def set_mint_tracker( ctx:discord.ApplicationContext, 
                            address:Option( str, 'Enter contract address of a collection.' ), 
                            token_name:Option( str, 'Give this token a name.' ),
                            total_supply:Option( str, 'Give this token its total supply.' +
                                                'You can use - instead if you don\'t need to know it.' ) ) -> None:
    ''' Set a tracker to watch one\'s collection mint status. (current total supply) '''
    global CFG, SCHEDULER, TRACKER

    if CFG.get_mint_tracker_channel() == 0:
        embed = make_embed( description = '您必須先設定鑄幣變動發送頻道 參考：`/bind`',
                            color = dc_color( 'red' ), thumbnail_url = CFG.get_error_img_url() )
        await ctx.respond( embed = embed )
        return
    # if

    cur_supply = TRACKER.current_token_supply( address )

    if ( cur_supply == '0' ):
        embed = make_embed( description = '非法合約地址或尚未開放 mint',
                            color = dc_color( 'red' ), thumbnail_url = CFG.get_error_img_url() )
        await ctx.respond( embed = embed )
        return
    # if

    if ( cur_supply == total_supply ):
        embed = make_embed( description = '本合約地址已達最大 mint 數，追蹤設置無效。',
                            color = dc_color( 'red' ), thumbnail_url = CFG.get_error_img_url() )
        await ctx.respond( embed = embed )
        return
    # if

    ( success, reason ) = SCHEDULER.add_mint_tracker( address, token_name, total_supply, cur_supply )

    if not success:
        embed = make_embed( description = reason, color = dc_color( 'red' ), thumbnail_url = CFG.get_error_img_url() )
        await ctx.respond( embed = embed )
        return
    # if

    fields = [['名稱', token_name, False],
              ['合約地址', f'[{address}](https://cronoscan.com/token/{address})', False],
              ['當前數量 / 最大供應', f'{cur_supply} / {total_supply}', False]
             ]

    embed = make_embed( description = '追蹤已設置成功', color = dc_color( 'green' ), 
                        thumbnail_url = CFG.get_done_img_url(), more_fields = fields )
    await ctx.respond( embed = embed )
    
# set_mint_tracker()

@delete.command( name = 'mint_tracker', description = 'Delete an existing mint tracker.' )
@commands.is_owner()
@commands.cooldown( 1, 15, commands.BucketType.user )
async def delete_mint_tracker( ctx:discord.ApplicationContext, 
                               address:Option( str, 'Enter a Ebisu\'s bay collection url which in the record.' ) ) \
                               -> None:
    ''' Delete an existing mint tracker from the mint tracker list. '''
    global SCHEDULER, TRACKER
    
    ( success, reason ) = SCHEDULER.delete_mint_tracker( address )

    if not success:
        embed = make_embed( description = reason, color = dc_color( 'red' ), thumbnail_url = CFG.get_error_img_url() )
        await ctx.respond( embed = embed )
    # if

    else:
        description = f'已取消追蹤此合約地址：[{address}](https://cronoscan.com/token/{address})'
        embed = make_embed( description = description, color = dc_color( 'green' ),
                            thumbnail_url = CFG.get_done_img_url() )
        await ctx.respond( embed = embed )
    # else
# delete_mint_tracker()

@list.command( name = 'all_mint_trackers', description = 'List all mint trackers.' )
@commands.cooldown( 1, 15, commands.BucketType.user )
async def list_all_mint_trackers( ctx:discord.ApplicationContext ) -> None:
    ''' List all mint trackers '''
    global SCHEDULER

    track_pages = []
    page_num = 0

    t_embed = discord.Embed( title = '', description = '當前所有鑄幣追蹤清單', color = dc_color('purple') )
    trackers = SCHEDULER.get_mint_trackers()

    if len( trackers ) == 0:
        await ctx.respond( embed = t_embed )
        return
    # if

    i = 0

    for tracker in trackers:
        i += 1

        t_embed.add_field( name = '名稱', value = tracker.token_name, inline = False )
        t_embed.add_field( name = '合約地址', 
                           value = f'[{tracker.contract_addr}](https://cronoscan.com/token/{tracker.contract_addr})',
                           inline = True )
        t_embed.add_field( name = '當前數量 / 最大供應', 
                           value = f'{tracker.cur_supply} / {tracker.total_supply}',
                           inline = True )
        
        if i % 3 == 0:
            page_num = i // 3
            new_page = Page( content = f'Page {page_num} / ', embeds = [t_embed] )
            track_pages.append( new_page )
            t_embed = discord.Embed( title = '', description = '當前所有鑄幣追蹤清單', color = dc_color('purple') )
        # if
    # for

    if i % 3 > 0:
        page_num += 1
        new_page = Page( content = f'Page {page_num} / ', embeds = [t_embed] )
        track_pages.append( new_page )
    # if
    
    total_jobs = len( track_pages )

    for page in track_pages:
        page.content += str( total_jobs )

    paginator = Paginator( pages = track_pages, loop_pages = True, disable_on_timeout = True, show_indicator = False,
                           use_default_buttons = False, custom_buttons = page_buttons, timeout = 60 )
    await paginator.respond( ctx.interaction )
    
# list_all_mint_trackers()

@bot.slash_command( name = 'choose', description = 'Choose one of the given options.' )
@commands.cooldown( 1, 5, commands.BucketType.user )
async def choose( ctx:discord.ApplicationContext, *, 
                  options:Option( str, 'Enter your options separated by , or space.' ) ) -> None:
    ''' Choose a option from user given. '''
    global CFG

    choices = ''

    if ',' in options:
        choices = options.replace( ' ', '' ).split( ',' )
    else:
        choices = options.split()

    choice = random.choice( choices )
    choices_title = ''

    for i, choice_str in enumerate( choices ):
        choices_title = choices_title + str( i + 1 ) + '. ' + choice_str + ', '
    choices_title = choices_title[:-2]

    embed =  make_embed( description = choices_title, color = dc_color( 'purple' ),
                         thumbnail_url = CFG.get_choose_img_url(), more_fields = [['選擇', choice, False]] )
    await ctx.respond( embed = embed )
# choose()

@bot.slash_command( name = 'fishing', description = 'Go to bay and test your luck today by fishing.' )
@commands.cooldown( 1, 72000, commands.BucketType.user ) # will change cd to 22 hr
async def fishing( ctx:discord.ApplicationContext ) -> None:
    ''' Test your luck today by fishing. '''
    global CFG, SCHEDULER, MAIN_LOGGER

    embed =  make_embed( title = '釣魚占卜 :fishing_pole_and_fish:',
                         description = '選擇您想前往釣魚占卜的地方 :arrow_right:', color = dc_color( 'purple' ),
                         thumbnail_url = CFG.get_choose_img_url() )

    ( success_e, result_east ) = SCHEDULER.fetch_ramdom_record_from( 'EAST' )
    ( success_w, result_west ) = SCHEDULER.fetch_ramdom_record_from( 'WEST' )
    ( success_s, result_south ) = SCHEDULER.fetch_ramdom_record_from( 'SOUTH' )
    ( success_n, result_north ) = SCHEDULER.fetch_ramdom_record_from( 'NORTH' )

    success = ( success_e and success_w and success_s and success_n )

    if not success:
        embed.description = '看來河神的釣竿似乎壞掉了...(連線或參數異常)'
        embed.set_thumbnail( url = CFG.get_error_img_url() )
        await ctx.respond( embed = embed )
        MAIN_LOGGER.error( '資料庫連線或參數異常' )
        return
    # if

    result = { 'EAST':result_east, 'WEST':result_west, 'SOUTH':result_south, 'NORTH':result_north }
    divination_card = FishingView( ctx.author.id, result, CFG.get_fishing_img_url() )
    await ctx.respond( embed = embed, view = divination_card )

# fishing()

@bot.slash_command( name = 'wish', description = 'Wishing for the birth of new fish in the bay.' )
@commands.cooldown( 1, 72000, commands.BucketType.user ) # will change cd to 22 hr
async def wish( ctx:discord.ApplicationContext ) -> None:
    ''' Wishing for the birth of new fish in the bay. '''
    global CFG

    wishform = FishingWishForm( title = '許願卡' )
    await ctx.send_modal( wishform )
# wish()

##### status: not completed
@sys.command( name = 'status', description = 'Check the bot status.' )
@commands.cooldown( 1, 60, commands.BucketType.user )
async def status( ctx:discord.ApplicationContext ):
    ''' Check the bot status. '''
    global CFG, TRACKER

    # cronos api, cmc api
    cronos_api_status = TRACKER.cronos_api_status()
    cmc_api = True # not completed
    service_status = cronos_api_status and cmc_api and track_mint_status.is_running() and track_floor_price.is_running()

    status_color = dc_color( 'green' ) if service_status else dc_color( 'red' )
    desc = ':green_circle: 正常運作中。' if service_status else ':red_circle: 以下服務連線不穩或中斷。'
    img_url = CFG.get_done_img_url() if service_status else CFG.get_error_img_url()

    if not cronos_api_status:
        desc += '\nCronos API'
    if not cmc_api:
        desc += '\nCMC API'
    if not track_mint_status.is_running():
        desc += '\nTask: Mint tracker'
    if not track_floor_price.is_running():
        desc += '\nTask: Floor tracker'

    embed = make_embed( title = f'響應時間: `{int( bot.latency * 1000 )} ms`', description = desc,
                        color = status_color, thumbnail_url = img_url )
    await ctx.respond( embed = embed )
# status()

@sys.command( name = 'start_mint_tracker_task', description = 'To execute mint tracker task.' )
@commands.is_owner()
async def start_mint_tracker_task( ctx:discord.ApplicationContext ):
    ''' Start mint_tracker executing task. '''
    global CFG

    channel = await bot.fetch_channel( CFG.get_system_log_channel() )
    desc = ''

    if not track_mint_status.is_running():
        track_mint_status.start()
        desc = '已啟動鑄幣追蹤任務迴圈'
        color = dc_color( 'green' )
    # if
    else:
        desc = '鑄幣追蹤任務迴圈已在運作狀態'
        color = dc_color( 'l_blue' )
    # else

    embed = make_embed( description = desc, color = color, thumbnail_url = CFG.get_done_img_url() )
    await channel.send( embed = embed )
# start_mint_tracker_task()

@sys.command( name = 'stop_mint_tracker_task', description = 'Stop executing mint tracker task.' )
@commands.is_owner()
async def stop_mint_tracker_task( ctx:discord.ApplicationContext ):
    ''' Stop mint_tracker executing task. '''
    global CFG

    channel = await bot.fetch_channel( CFG.get_system_log_channel() )
    desc = ''

    if track_mint_status.is_running():
        track_mint_status.start()
        desc = '已暫停鑄幣追蹤任務迴圈'
        color = dc_color( 'green' )
    # if
    else:
        desc = '鑄幣追蹤任務迴圈已在停止狀態'
        color = dc_color( 'l_blue' )
    # else

    embed = make_embed( description = desc, color = color, thumbnail_url = CFG.get_done_img_url() )
    await channel.send( embed = embed )
# stop_mint_tracker_task()

@sys.command( name = 'start_floor_tracker_task', description = 'To execute floor tracker(job) task.' )
@commands.is_owner()
async def start_floor_tracker_task( ctx:discord.ApplicationContext ):
    ''' Start floor_tracker executing task. '''
    global CFG

    channel = await bot.fetch_channel( CFG.get_system_log_channel() )
    desc = ''

    if not track_floor_price.is_running():
        track_floor_price.start()
        desc = '已啟動地板價追蹤任務迴圈'
        color = dc_color( 'green' )
    # if
    else:
        desc = '地板價追蹤任務迴圈已在運作狀態'
        color = dc_color( 'l_blue' )
    # else

    embed = make_embed( description = desc, color = color, thumbnail_url = CFG.get_done_img_url() )
    await channel.send( embed = embed )
# start_floor_tracker_task()

@sys.command( name = 'stop_floor_tracker_task', description = 'Stop executing mint tracker task.' )
@commands.is_owner()
async def stop_floor_tracker_task( ctx:discord.ApplicationContext ):
    ''' Stop floor_tracker executing task. '''
    global CFG

    channel = await bot.fetch_channel( CFG.get_system_log_channel() )
    desc = ''

    if track_floor_price.is_running():
        track_floor_price.start()
        desc = '已暫停地板價追蹤任務迴圈'
        color = dc_color( 'green' )
    # if
    else:
        desc = '地板價追蹤任務迴圈已在停止狀態'
        color = dc_color( 'l_blue' )
    # else

    embed = make_embed( description = desc, color = color, thumbnail_url = CFG.get_done_img_url() )
    await channel.send( embed = embed )
# stop_floor_tracker_task()

@sys.command( name = 'shutdown', description = 'Shutdown this bot.' )
@commands.is_owner()
async def shutdown( ctx:discord.ApplicationContext ):
    ''' Shutdown this bot. '''
    global CFG, SCHEDULER, MAIN_LOGGER, TRACKER

    embed = make_embed( description = '本服務將於 5 秒後停機，暫停使用。', color = dc_color( 'purple' ) )
    sent_msg = await ctx.respond( embed = embed )

    disconnect_event = SCHEDULER.rest()
    MAIN_LOGGER.info( disconnect_event )
    task_loop( 'stop' )

    if TRACKER.browser_is_running:
        await TRACKER.close_browser()

    await asyncio.sleep( 5 )

    embed = make_embed( description = '機器人已關機', color = dc_color( 'purple' ), 
                        thumbnail_url = CFG.get_hello_and_bye_img_url() )
    await sent_msg.edit_original_message( embed = embed )

    await ctx.bot.close()
    MAIN_LOGGER.info( '機器人已關機' )
    
# shutdown()

@convert.command( name = 'to_usd', description = 'Convert CRO value to USD.' )
@commands.cooldown( 1, 15, commands.BucketType.user )
async def convert_cro( ctx:discord.ApplicationContext,
                       cro:Option( float, 'Enter a value in CRO you want.' ) ) -> None:
    ''' Convert CRO value to USD. '''
    global CMCFUNC

    if cro < 0:
        embed = make_embed( description = '非法數值，請勿輸入負數!', color = dc_color( 'red' ) )

    elif cro == 0:
        embed = make_embed( description = '`0 CRO` <:arrow:1002316255736369192> `0 USD`', color = dc_color( 'l_blue' ) )
    
    else:
        price = CMCFUNC.cro_to_usd()

        if price == -1:
            embed = make_embed( description = '無法從 CMC API 獲取最新價格資訊，請使用 `/sys status` 檢查狀態',
                                color = dc_color( 'red' ) )
        # if
        else:
            price *= cro
            embed = make_embed( description = f'`{cro} CRO` <:arrow:1002316255736369192> `{price} USD`',
                                color = dc_color( 'l_blue' ))
        # else
    # else

    await ctx.respond( embed = embed )
# convert_cro()

@convert.command( name = 'to_cro', description = 'Convert USD value to CRO.' )
@commands.cooldown( 1, 15, commands.BucketType.user )
async def convert_usd( ctx:discord.ApplicationContext,
                       usd:Option( float, 'Enter a value in USD you want.' ) ) -> None:
    ''' Convert USD value to CRO. '''
    global CMCFUNC

    if usd < 0:
        embed = make_embed( description = '非法數值，請勿輸入負數!', color = dc_color( 'red' ) )

    elif usd == 0:
        embed = make_embed( description = '`0 USD` <:arrow:1002316255736369192> `0 CRO`', color = dc_color( 'l_blue' ) )
    
    else:
        price = CMCFUNC.usd_to_cro()

        if price == -1:
            embed = make_embed( description = '無法從 CMC API 獲取最新價格資訊，請使用 `/sys status` 檢查狀態',
                                color = dc_color( 'red' ) )
        # if
        else:
            price *= usd
            embed = make_embed( description = f'`{usd} USD` <:arrow:1002316255736369192> `{price} CRO`',
                                color = dc_color( 'l_blue' ))
        # else
    # else

    await ctx.respond( embed = embed )
# convert_usd()

@bot.event
async def on_application_command_error( ctx:discord.ApplicationContext, error ) -> None:
    ''' Discord Application Command Error Handler '''

    if isinstance( error, commands.CommandNotFound ):
        return

    elif isinstance( error, commands.NotOwner ):
        await ctx.respond( '您須擁有權限: Owner 。' )
        return

    elif isinstance( error, commands.MissingRequiredArgument ):
        return

    elif isinstance( error, commands.CommandOnCooldown ):
        waiting_time = int( error.retry_after )

        if waiting_time < 60:
            await ctx.respond( f'{ctx.author.mention} 指令冷卻中，請等待 {waiting_time} 秒後再試。' )
        elif waiting_time < 3600:
            await ctx.respond( f'{ctx.author.mention} 指令冷卻中，' +
                               f'請等待 {waiting_time // 60} 分 {waiting_time % 60} 秒後再試。' )
        else:
            waiting_time //= 60
            await ctx.respond( f'{ctx.author.mention} 指令冷卻中，' +
                               f'請等待 {waiting_time // 60} 小時 {waiting_time % 60} 分後再試。' )
        
        return
    # elif

    else:
        raise error
# on_application_command_error()


''' Discord Tasks Below'''

error_times_on_tm = 0

@tasks.loop( seconds = 5 )
async def track_mint_status():
    ''' Track all mint status by TRACKER '''
    global CFG, SCHEDULER, TRACKER, MAIN_LOGGER, error_times_on_tm

    trackers = SCHEDULER.get_mint_trackers()

    if len( trackers ) == 0:
        return

    channel = await bot.fetch_channel( CFG.get_mint_tracker_channel() )

    for tracker in trackers:
        cur_supply = TRACKER.current_token_supply( tracker.contract_addr )

        if cur_supply == '':
            error_times_on_tm += 1
            MAIN_LOGGER.warning( f'暫時無法取得:{tracker.contract_addr} 此合約資訊!' )

            if error_times_on_tm >= 3:
                error_times_on_tm = 0
                track_mint_status.stop()
                MAIN_LOGGER.error( f'Cronos API 連續多次請求失敗，已停止本任務!' )   
            # if
            return
        # if
        else:
            error_times_on_tm = 0

        try:
            new_supply_int = int( cur_supply )
            old_supply_int = int( tracker.cur_supply )
        # try
        except Exception as e:
            MAIN_LOGGER.warning( e )
            return
        # except

        if new_supply_int > old_supply_int:
            # Renew total supply and display it on discord
            old_cur_supply = tracker.cur_supply
            new_cur_supply = cur_supply

            ( success, reason ) = SCHEDULER.update_tracker( tracker.contract_addr, new_cur_supply )

            if not success:
                MAIN_LOGGER.warning( reason )
                track_mint_status.stop()
                embed = make_embed( description = 'Mint 數量無法更新至資料庫，任務已終止。', color = dc_color( 'red' ),
                                    thumbnail_url = CFG.get_error_img_url() )
                await channel.send( embed = embed )
                return
            # if

            mint_out = True if tracker.cur_supply == tracker.total_supply else False

            embed = make_embed( title = 'Mint 數量更新! 🔥🔥🔥',
                                color = dc_color( 'l_blue' ),
                                thumbnail_url = CFG.get_floor_change_img_url(),
                                more_fields = [['名稱', f'`{tracker.token_name}`', False ],
                                               ['最大供應', f'`{tracker.total_supply}`', False ],
                                               ['供應變化', f'`{old_cur_supply}` <:arrow:1002316255736369192> ' +
                                                            f'`{new_cur_supply}`', False]
                                              ]
                                )
            view = TrackerMsgView()
            check_button = discord.ui.Button( label = 'Check', style = discord.ButtonStyle.link, 
                                              url = f'https://cronoscan.com/token/{tracker.contract_addr}' )
            view.add_item( check_button )
            await channel.send( embed = embed, view = view )

            if mint_out:
                ( success, reason ) = SCHEDULER.delete_mint_tracker( tracker.contract_addr )

                if not success:
                    embed = make_embed( title = 'Mint 完售!(發生內部錯誤)',
                                        description = f'{tracker.token_name} 已成功結束 Mint，' +
                                                      '然本追蹤任務撤銷時發生意外，任務已終止，請檢驗log。',
                                        color = dc_color( 'red' ), thumbnail_url = CFG.get_error_img_url() )
                    await channel.send( embed = embed, view = view )
                    MAIN_LOGGER.warning( reason )
                    track_mint_status.stop()
                    return
                # if

                else:
                    embed = make_embed( title = 'Mint 完售! 🔥🔥🔥🔥🔥',
                                        description = f'{tracker.token_name} 已成功結束 Mint，本追蹤任務已永久撤銷。',
                                        color = dc_color( 'purple' ), thumbnail_url = CFG.get_done_img_url() )
                    await channel.send( embed = embed, view = view )
                # else
            # if
        # if
        
    # for
# track_mint_status()

error_times_on_fp = 0

@tasks.loop( minutes = 3 )
async def track_floor_price():
    ''' Track all floor price by TRACKER '''
    global CFG, SCHEDULER, TRACKER, MAIN_LOGGER, error_times_on_fp

    jobs = SCHEDULER.get_jobs()

    if len( jobs ) == 0:
        return

    channel = await bot.fetch_channel( CFG.get_floor_tracker_channel() )

    for job in jobs:
        ( screenshot_path, new_floor_price ) = await TRACKER.track_with_detail( job.type, job.eb_url )

        if screenshot_path == '' and new_floor_price == '':
            error_times_on_fp += 1
            MAIN_LOGGER.warning( f'無法取得: <{job.eb_url}> 頁面資訊!' )

            if error_times_on_fp >= 3:
                error_times_on_fp = 0
                track_mint_status.stop()
                MAIN_LOGGER.error( f'爬蟲連續多次請求失敗，已停止本任務!' )
            # if
            return
        # if
        else:
            error_times_on_fp = 0

        if new_floor_price != '' and new_floor_price != job.cur_floor:
            # Update new floor price and display it on discord
            old_cur_floor = job.cur_floor

            ( success, reason ) = SCHEDULER.update_job( job.eb_url, new_floor_price )
            
            if not success:
                MAIN_LOGGER.warning( reason )
                track_floor_price.stop()
                embed = make_embed( description = '地板價無法更新至資料庫，任務已終止。',
                                  color = dc_color( 'red' ), thumbnail_url = CFG.get_error_img_url() )
                await channel.send( embed = embed )
                return
            # if

            if job.type == '721':
                file = discord.File( screenshot_path )

                embed = make_embed( title = '地板價更新! (ERC721) 🔥🔥🔥', color = dc_color( 'l_blue' ),
                                    thumbnail_url = CFG.get_floor_change_img_url(),
                                    more_fields = [['地板價變化', f'`{old_cur_floor}` <:arrow:1002316255736369192> ' +
                                                                f'`{job.cur_floor}`', False]],
                                    is_local_image = True, image_url = f'attachment://{screenshot_path}' )
                view = TrackerMsgView()
                check_button = discord.ui.Button( label = 'Check', style = discord.ButtonStyle.link, url = job.eb_url )
                view.add_item( check_button )
                await channel.send( content = f'地板價更新通知! {job.mention_target}',
                                    file = file, embed = embed, view = view )
            # if
            else: # For now, it's 1155
                series = ( job.eb_url ).replace( 'https://app.ebisusbay.com/collection/', '' )
                embed = make_embed( title = '地板價更新! (ERC1155) 🔥🔥🔥', color = dc_color( 'l_blue' ),
                                    thumbnail_url = CFG.get_floor_change_img_url(),
                                    more_fields = [['名稱', series, False],
                                                   ['地板價變化', f'`{old_cur_floor}` <:arrow:1002316255736369192> ' +
                                                                f'`{job.cur_floor}`', False]] )
                view = TrackerMsgView()
                check_button = discord.ui.Button( label = 'Check', style = discord.ButtonStyle.link, url = job.eb_url )
                view.add_item( check_button )
                await channel.send( content = f'地板價更新通知! {job.mention_target}', embed = embed, view = view )
            # else
        # if

        if job.type == '721': # Only type ERC721 has screenshot on the system.
            try:  
                os.remove( f'{os.getcwd()}/{screenshot_path}' ) 
                MAIN_LOGGER.debug( f'{screenshot_path} 已被系統刪除!' )
                
            # try
            except OSError as e: 
                MAIN_LOGGER.warning( f'{screenshot_path} 無法被系統刪除!: {e}' )
        # if
    # for

# track_floor_price()

if __name__ == '__main__':
    main()