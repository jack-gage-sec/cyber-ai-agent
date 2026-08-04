def calculate_metrics(
    alerts,
    exceptions,
):

    return {

        "alerts":
            len(alerts),

        "critical":
            len(
                alerts[
                    alerts["severity"]
                    == "Critical"
                ]
            ),

        "exceptions":
            len(exceptions),

    }