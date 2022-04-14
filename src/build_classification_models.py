from .classification_models.lda_negativity import lda_negativity
from .classification_models.lda_net_predisposition import lda_net_predisposition
from .classification_models.lda_positivity import lda_positivity

from .classification_models.lr_negativity import lr_negativity
from .classification_models.lr_net_predisposition import lr_net_predisposition
from .classification_models.lr_positivity import lr_positivity


def build_classification_models():
    lda_negativity()
    lda_net_predisposition()
    lda_positivity()
    lr_negativity()
    lr_net_predisposition()
    lr_positivity()


if __name__ == "__main__":
    build_classification_models()