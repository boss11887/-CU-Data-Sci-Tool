import pandas as pd

def main():
    file = input()
    func = input()

    df = pd.read_csv(file)

    if func == 'Q1':
        print(df.shape)
    elif func == 'Q2':
        print(max(df['score']))
    elif func == 'Q3':
        print(df[df['score'] >= 80].shape[0])
    else:
        print('No Output')

if __name__ == "__main__":
    main()
