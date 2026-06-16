import matplotlib.pyplot as plt

def plot_recommendations(results):
    names = [
        m["name"]
        for m in results
    ]

    scores = [
        m["score"]
        for m in results
    ]

    plt.figure(figsize=(10, 6))
    plt.barh(names, scores)
    plt.xlabel("Similarity Score")
    plt.title(
        "Top Movie Recommendations"
    )
    plt.gca().invert_yaxis()
    return plt