import json
import numpy as np
import matplotlib.pyplot as plt

_NUM_QUESTIONS = 100
_MODEL1_NAME = 'bard'
_MODEL1_DIGEST = 'bard_digest'
_MODEL2_NAME = 'chatgpt3.5'
_MODEL2_DIGEST = 'chatgpt3.5_digest'
_MODEL3_NAME = 'llama2'
_MODEL3_DIGEST = 'llama2_digest'

# TODO: Add functions for converting txt to json (found in create outputs)


def get_data(in_file_name):
    with open(in_file_name) as f:
        return json.load(f)

def get_domain_names(data):
    domains = []
    try:
        for e in data['inputs']:
            if e['domain'] not in domains:
                domains.append(e['domain'])
    except Exception as inst:
        print(type(inst))
        print(inst)
        print("Probably no field called 'domain' in JSON (which is ok)")
    return domains

def get_model_accuracy(data, domain=''):
    number_correct = [0, 0, 0]
    total = 0
    for e in data['inputs']:
        if (domain == '') or (e['domain'] == domain):
            total += 1
            if e[_MODEL1_DIGEST] == e['author']:
                number_correct[0] += 1
            if e[_MODEL2_DIGEST] == e['author']:
                number_correct[1] += 1
            if e[_MODEL3_DIGEST] == e['author']:
                number_correct[2] += 1
    model_accuracy = [0., 0., 0.]
    if total > 0:
        for i in range(0, 3):
            model_accuracy[i] = (float(number_correct[i]) / total) * 100
    return model_accuracy

def get_domain_accuracies(data):
    domains = get_domain_names(data)
    # if n is the number of domains then domain accuracy will have shape (n x 3)
    domain_accuracy = []
    if len(domains) != 0:
        for d in domains:
            domain_accuracy.append(get_model_accuracy(data, d))
    return domain_accuracy

def output_metrics(data, out_file_name):
    total_accuracy = get_model_accuracy(data)
    domains = get_domain_names(data)
    with open(out_file_name, 'w+') as f:
        f.write("================================================================================\n|                               Model Accuracies                               |\n================================================================================\n\n")
        f.write('Total accuracies:\n')
        f.write('\t' + _MODEL1_NAME + ': ' + str(total_accuracy[0]) + '%\n')
        f.write('\t' + _MODEL2_NAME + ': ' + str(total_accuracy[1]) + '%\n')
        f.write('\t' + _MODEL3_NAME + ': ' + str(total_accuracy[2]) + '%\n')
        if len(domains) != 0:
            # if n is the number of domains then domain accuracy will have 
            # shape (n x 3)
            domain_accuracy = get_domain_accuracies(data)
            for i in range(len(domains)):
                f.write('\n================================================================================\n\n')
                f.write(domains[i] + ' Domain Accuracy:\n')
                f.write('\t' + _MODEL1_NAME + ': ' + str(domain_accuracy[i][0]) + '%\n')
                f.write('\t' + _MODEL2_NAME + ': ' + str(domain_accuracy[i][1]) + '%\n')
                f.write('\t' + _MODEL3_NAME + ': ' + str(domain_accuracy[i][2]) + '%\n')

def create_line_graphs(data):
    heatmap = np.ndarray((3, _NUM_QUESTIONS), dtype=int)
    i = 0
    for e in data['inputs']:
        if e[_MODEL1_DIGEST] == e['author']:
            heatmap[0, i] = 1
        else:
            heatmap[0, i] = 0
        if e[_MODEL2_DIGEST] == e['author']:
            heatmap[1, i] = 1
        else:
            heatmap[1, i] = 0
        if e[_MODEL3_DIGEST] == e['author']:
            heatmap[2, i] = 1
        else:
            heatmap[2, i] = 0
        i += 1
    questions = np.arange(1, _NUM_QUESTIONS + 1)
    # average_response = np.mean(heatmap, axis=0)
    normalized_correct = np.sum(heatmap, axis=0) / 3
    fig, axs = plt.subplots(3, 1, figsize=(10, 12))
    axs[0].plot(questions, heatmap[0, :], label=_MODEL1_NAME)
    axs[0].set_ylabel('Correct')
    axs[0].set_title(_MODEL1_NAME + ' Performance')
    axs[0].set_yticks(np.arange(0, 1.1, step=1))
    
    axs[1].plot(questions, heatmap[1, :], label=_MODEL2_NAME)
    axs[1].set_ylabel('Correct')
    axs[1].set_title(_MODEL2_NAME + ' Performance')
    axs[1].set_yticks(np.arange(0, 1.1, step=1))
    
    axs[2].plot(questions, heatmap[2, :], label=_MODEL3_NAME)
    axs[2].set_ylabel('Correct')
    axs[2].set_title(_MODEL3_NAME + ' Performance')
    axs[2].set_yticks(np.arange(0, 1.1, step=1))
    
    plt.tight_layout()
    plt.savefig('line_graphs.png')
    plt.show()

def create_bar_graph(data):
    # Create a bar graph showing the accuracy of each model in each domain (and 
    #   overall)
    domains = get_domain_names(data)
    accuracy = np.ndarray((3, 1 + len(domains)), dtype=float)
    accuracy[:, 0] = np.array(get_model_accuracy(data))
    for i in range(len(domains)):
        accuracy[:, i+1] = np.array(get_model_accuracy(data, domains[i]))
    
    x = np.arange(np.shape(accuracy)[1])
    width = 0.25
    fig, ax = plt.subplots(figsize=(10, 6))
    r1 = ax.bar(x - width, accuracy[0, :], width, label=_MODEL1_NAME.capitalize())
    r2 = ax.bar(x, accuracy[1, :], width, label=_MODEL2_NAME.capitalize())
    r3 = ax.bar(x + width, accuracy[2, :], width, label=_MODEL3_NAME.capitalize())
    ax.set_title('Comparing Accuracies of Each Model')
    ax.set_xlabel('Domain')
    ax.set_ylabel('Accuracy (%)')
    ax.set_xticks(x)
    ax.set_xticklabels(['Total'] + domains)
    ax.legend()

    plt.tight_layout()
    plt.savefig('bar_graph.png')
    plt.show()

    # Now create average bar graph
    mean_accuracy = np.mean(accuracy, axis=0)
    plt.figure(figsize=(10, 6))
    plt.bar(x, mean_accuracy)
    plt.xlabel('Domain')
    plt.ylabel('Accuracy (%)')
    plt.title('Bar Graph Showing Mean Accuracy of the Three Models')
    plt.xticks(x, ['Total'] + domains)
    plt.savefig('bar_graph_mean.png')
    plt.show()

def main():
    data = get_data('outputs.json')
    output_metrics(data, 'metrics.txt')
    create_line_graphs(data)
    create_bar_graph(data)

if __name__ == '__main__':
    main()
