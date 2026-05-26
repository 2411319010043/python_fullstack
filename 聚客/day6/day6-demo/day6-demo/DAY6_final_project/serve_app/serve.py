from fastapi import FastAPI
from langserve import add_routes

from DAY6_final_project.few_shot.selector_few_shot import chain as selector_chain
from DAY6_final_project.few_shot.fixed_few_shot import chain as fixed_chain
from DAY6_final_project.chat_history.history_chat import chain_with_history as history_chain
from DAY6_final_project.final_chat import final_chain
app = FastAPI()

add_routes(app, final_chain, path="/chat")
add_routes(app, selector_chain, path="/selector")
add_routes(app, fixed_chain, path="/fixed")
add_routes(app, history_chain, path="/history")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8012)