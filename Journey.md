
# Hi Steffen Hi Marcel

I will add my journey and assumptions here so you can follow my thought process.

* As this is a toy backend, I am sometimes using files as directories, e.g., outbound, service, apis.
* I am assuming the topic endpoints are not hotel-customer-facing but rather hotel-staff-facing. I imagine these endpoints being called from the dashboard, not for searching one’s past conversations. In that case, a more flexible topic search with embedding search would be appropriate. My assumption is based on the endpoints being called analytics and the task being roughly 2 hours. BTW, it took me longer, if you must know ;)
* I decided to make the set of topics fixed, and the client should know what to ask for. I also decided to keep the fixed set in the database rather than in code. I think in code they look like they can be refactored without a migration.
* I use in-memory DBs for now, but they are Mongo-style.
* Some missing components that could be added next: global and local error handling, returning mapped error responses, REST layer models (for now I used untyped dicts), and adding service layer tests. Since I do not use separate DB containers, it is all the same.
* For generating topics, I use an LLM API, nothing fancy. I imagine when we also have an “add conversation” endpoint, the “add topic” would be called asynchronously, once per added conversation.
* I am more or less using patterns we used for SpringBoot, like ServiceFactory. I am open to learning more approaches that are more common with FastAPI.
* The local ServiceFactory is basically simulating past DB state based on the JSON you provided.
* I suspect I have forgotten types here and there. I am used to types being enforced, not optional. Curious to see how you deal with this so that it is more automatic, or checked by a linter.

