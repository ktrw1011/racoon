import pickle
import shutil
from typing import Optional
from pathlib import Path

import pandas as pd

class ExpManager:
    def __init__(self,
        root_exp_dir:Optional[Path]=None,
        ) -> None:
        """[summary]

        Args:
            root_exp_dir (Optional[Path], optional): 実験ルートディレクトリ。デフォルトでカレントディレクトリ
            exp_name (Optional[str], optional): 実験名。デフォルトで
        """

        self.root_exp_dir = root_exp_dir
        if root_exp_dir is None:
            self.root_exp_dir= Path.cwd()

        self.name = None
        self.version = None
        self.exp_dir = None
        self.features_dir = None
        self.output_dir = None

    def init(self, name:Optional[str]=None):
        if self.version is not None:
            raise ValueError("It's already initialized")

        self.version = self.next_exp_version()

        if self.name is None:
            self.exp_dir = self.root_exp_dir / ('exp-' + self.version)
        else:
            self.exp_dir = self.root_exp_dir / ('exp-' + self.version + "-" + self.name)

        self.features_dir = self.exp_dir / 'features'
        self.output_dir = self.exp_dir / 'output'

        self.features_dir.mkdir(exist_ok=True, parents=True)
        self.output_dir.mkdir(exist_ok=True, parents=True)

        print(self)

    def start(self):
        self.version = self.root_exp_dir.name

        self.exp_dir = self.root_exp_dir
        self.features_dir = self.exp_dir / 'features'
        self.output_dir = self.exp_dir / 'output'

        print(self)

    def read(self, version:Optional[int]=None):

        try:
            exp_dir = list((self.root_exp_dir).glob(f'exp-{version}'))[0]
        except IndexError:
            raise ValueError(f"Not Found Experiment Version {version}")

        self.exp_dir = exp_dir
        self.features_dir = self.exp_dir / 'features'
        self.output_dir = self.exp_dir / 'output'

        print(self)

    def __repr__(self) -> str:
        if self.exp_dir is None:
            return f"root experiment directory: {str(self.root_exp_dir)::>10}\n"\
                f"experiment directory is not initialized"
        else:
            return f"root experiment directory: {str(self.root_exp_dir)::>10}\n"\
                f"{'experiment version'}: {str(self.exp_dir.name):>10}\n"\
                f"{'features directory'}: {str(self.features_dir.stem):>10}\n"\
                f"{'output directory'}: {str(self.output_dir.stem):>10}\n"

    def _get_current_file_path(self) -> str:
        try:
            import ipynb_path
            return ipynb_path.get()
        except:
            raise ValueError

    def next_exp_version(self) -> int:
        version = self.newest_exp_version()
        return str(version+1)

    def newest_exp_version(self) -> int:

        exps = list((self.root_exp_dir).glob('exp-*'))
        exps_dir = [p for p in exps if p.is_dir()]
        if len(exps_dir) == 0:
            return 0
        else:
            vers = list(map(lambda x: int(str(x).split('-')[1]), exps_dir))
            vers = sorted(vers)[::-1][0]

        return int(vers)

    def sweep(self, feature=True, output=True) -> None:
        if feature:
            shutil.rmtree(self.features_dir)
            self.features_dir.mkdir(exist_ok=False)
            print('[Swept Features Directory]')
        else:
            shutil.rmtree(self.output_dir)
            self.features_dir.mkdir(exist_ok=False)
            print('[Swept Output Directory]')

    def store_feature(self, name:str, input_df:pd.DataFrame) -> None:
        name = name + '.pkl'
        with open(self.features_dir / name, 'wb') as f:
            pickle.dump(input_df, f)

        print(f'[Save Feature]: {name}')

    def load_feature(self, name:str) -> pd.DataFrame:
        name = name + '.pkl'
        with open(self.features_dir / name, 'rb') as f:
            print(f'[Load Feature]: {name}')
            return pickle.load(f)

    def load_features(self) -> pd.DataFrame:
        _dfs = []
        for path in self.features_dir.glob('*.pkl'):
            with open(path, 'rb') as f:
                print(f'[Load Feature]: {path.name}')
                _dfs.append(pickle.load(f))

        return pd.concat(_dfs, axis=1)