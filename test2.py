from winotify import Notification

toast = Notification(app_id="example app",
                     title="Winotify Test Toast",
                     msg="New Notification!")

toast.add_actions(label="Button text",
                  link="https://github.com")

toast.add_actions(label="Button text2",
                  link="https://github.com")

toast.build().show()