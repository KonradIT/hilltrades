import flask

from capitoltrades import CapitolTrades

app = flask.Flask(__name__)

@app.route("/get-pids")
def get_pids():
    """See the map of all the known politicians mapped to their IDs for capitoltrades.com.
    Can be used to query the `by_pid` endpoint."""
    capitol = CapitolTrades()
    return flask.jsonify(capitol.politicians)

@app.route("/by-name/<name>", methods=["GET"])
def by_name(name):
    """Query all of the politicians trades by their name. Returns the first match to the given name. Not the most accurate,
    so we suggest finding the ID with `get_pids()` first, then querying the `by_pid()` endpoint."""
    capitol = CapitolTrades()
    pid = capitol.get_politician_id(name)
    if not pid:
        return flask.jsonify({
            "status": "error",
            "message": "No match found for search term {}.".format(name)
        })
    else:
        return by_pid(pid)

@app.route("/by-pid/<pid>", methods=["GET"])
def by_pid(pid):
    """Query all of the politicians trades by their politician ID assigned by capitoltrades.com"""
    capitol = CapitolTrades()
    try:
        trades = capitol.trades(pid)
    except AssertionError:
        return flask.jsonify({
            "status": "error",
            "message": "No match found for the provided politician ID of {}.".format(pid),
        })
    
    return flask.jsonify(trades)
