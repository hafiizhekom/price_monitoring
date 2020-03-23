
from apscheduler.schedulers.blocking import BlockingScheduler
from data.app import Data

class Scheduler():
  def schedule(self):
    data = Data('data/db/db.json')
    print('This job is run every hours.')
    for url in data.getUrl():
      data.updatePrice(url, data.crawlPrice(url))

if __name__ == '__main__':
  scheduler = BlockingScheduler()
  scheduler.add_job(Scheduler().schedule, 'interval', hours=1)
  scheduler.start()

