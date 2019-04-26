<?php

namespace App\Model;

use Nette;

class InvertedModel extends BaseDocumentsModel {

    public function getSimilarDocuments($id) {
        // Run our python script in order to get similar docs
        exec("python3 ../../web_search.py" . " inverted " . $id, $out, $status);

        // out - [0] => path of called script, [1] => result of script
        $json = $out[0];
        $spentTime = $out[1];

        $similarDocs = json_decode($json, true);

        foreach ($similarDocs['docs'] as &$doc) {
            $docId = $doc[0];
            $doc[] = $this->getDocumentName($docId);
        }

        return [$similarDocs, $spentTime];
    }
}